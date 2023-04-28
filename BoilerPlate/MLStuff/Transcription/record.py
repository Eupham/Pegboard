#record.py
#sudo apt-get install portaudio19-dev

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

from pathlib import Path

if __name__ == '__main__':
    # Create the output directory if it doesn't already exist
    Path("output").mkdir(exist_ok=True)

    # Record audio until the escape key is pressed
    i = 0
    while True:
        # Generate a unique filename for this recording
        filename = f"recording_{i}.wav"
        filepath = Path("output") / filename
        recorder = AudioRecorder()

        # Record audio and save it to the output directory
        recorder.wave_output_filename = str(filepath)
        recorder.record_seconds = 15
        recorder.record_audio()

        print(f"Recording {i+1} complete. File saved to {filepath}")
        i += 1
