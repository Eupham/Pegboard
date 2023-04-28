#asr.py
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch
import torchaudio
import torch.utils.data as data
from pathlib import Path
import pyaudio
import wave
import numpy as np
import math

class AudioRecorder:
    def __init__(self, device_index=7, rate=16000, chunk=1024, record_seconds=10, mod_amp=5, wave_output_filename="output.wav"):
        self.device_index = device_index
        self.rate = rate
        self.chunk = chunk
        self.record_seconds = record_seconds
        self.mod_amp = mod_amp
        self.wave_output_filename = wave_output_filename

        self.audio = pyaudio.PyAudio()

    def record_audio(self):
        # open the audio stream
        stream = self.audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=self.rate,
                            input=True,
                            input_device_index=self.device_index,
                            frames_per_buffer=self.chunk)

        print("* recording")

        # create a buffer to store the audio data
        frames = []

        for i in range(0, round(self.rate / self.chunk * self.record_seconds)):
            data = stream.read(self.chunk)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        self.audio.terminate()

        audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)

        audio_data_mod = np.zeros(len(audio_data), dtype=np.int16)

        for i in range(len(audio_data)):
            audio_data_mod[i] = math.ceil(audio_data[i] * self.mod_amp)

        frames_mod = [audio_data_mod[i:i+self.chunk].tobytes() for i in range(0, len(audio_data_mod), self.chunk)]
        wf_mod = wave.open(self.wave_output_filename, 'wb')
        wf_mod.setnchannels(1)
        wf_mod.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wf_mod.setframerate(self.rate)
        wf_mod.writeframes(b''.join(frames_mod))
        wf_mod.close()

        print("* done recording")



class AudioTranscription:
    def __init__(self, model_name):
        self.processor = Wav2Vec2Processor.from_pretrained(model_name)
        self.model = Wav2Vec2ForCTC.from_pretrained(model_name, from_tf=False)

        
    def transcribe_audio(self, audio_file):
        waveform, sample_rate = torchaudio.load(audio_file)
        resampler = torchaudio.transforms.Resample(sample_rate, 16000)
        waveform = resampler(waveform)
        input_values = waveform.squeeze().to(torch.float32)
        input_values /= torch.max(torch.abs(input_values))
        logits = self.model(input_values.unsqueeze(0)).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.decode(predicted_ids[0])
        return transcription
    
import queue
import threading
import time

if __name__ == '__main__':
    output_folder = Path('output')
    output_folder.mkdir(exist_ok=True)
    file_queue = queue.Queue()

    def record():
        i = 0
        while True:
            # Generate a unique filename for this recording
            filename = f"recording_{i}.wav"
            filepath = Path("output") / filename
            
            recorder = AudioRecorder()

            # Record audio and save it to the output directory
            recorder.wave_output_filename = str(filepath)
            recorder.record_audio()

            file_queue.put(str(filepath))
            i += 1

    def transcribe():
        while True:
            if not file_queue.empty():
                audio_file = file_queue.get()
                audio_transcription = AudioTranscription('facebook/wav2vec2-large-960h-lv60-self')
                transcription = audio_transcription.transcribe_audio(audio_file)
                with open('transcripts.txt', 'a') as f:
                    f.write(transcription + '\n')
                
            # Limit the number of recordings in the queue to avoid excessive memory usage
            if file_queue.qsize() > 10:
                time.sleep(5) # Wait for 5 seconds before checking the queue again

    
    record_thread = threading.Thread(target=record)
    transcribe_thread = threading.Thread(target=transcribe)

    record_thread.start()
    transcribe_thread.start()

    while True:
        time.sleep(1)
