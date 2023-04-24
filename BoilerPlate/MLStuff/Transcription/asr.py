import pyaudio
import wave
import numpy as np
import math

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 10
MOD_AMP = 5
WAVE_OUTPUT_FILENAME = "output.wav"

# set the index of the USB audio device
device_index = 7

# create the audio object
p = pyaudio.PyAudio()

# open the audio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=CHUNK)

print("* recording")

# create a buffer to store the audio data
frames = []

for i in range(0, round(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

stream.stop_stream()
stream.close()
p.terminate()

audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)

audio_data_mod = np.zeros(len(audio_data), dtype=np.int16)

for i in range(len(audio_data)):
    audio_data_mod[i] = math.ceil(audio_data[i] * MOD_AMP)

frames_mod = [audio_data_mod[i:i+CHUNK].tobytes() for i in range(0, len(audio_data_mod), CHUNK)]
wf_mod = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf_mod.setnchannels(CHANNELS)
wf_mod.setsampwidth(p.get_sample_size(FORMAT))
wf_mod.setframerate(RATE)
wf_mod.writeframes(b''.join(frames_mod))
wf_mod.close()

print("* done recording")

from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch
import torchaudio

processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h-lv60-self", from_tf=False)

audio_file = "output.wav"
waveform, sample_rate = torchaudio.load(audio_file)

resampler = torchaudio.transforms.Resample(sample_rate, 16000)
waveform = resampler(waveform)

input_values = waveform.squeeze().to(torch.float32)
input_values /= torch.max(torch.abs(input_values))

logits = model(input_values.unsqueeze(0)).logits

predicted_ids = torch.argmax(logits, dim=-1)
transcription = processor.decode(predicted_ids[0])
print(transcription)

import torch.utils.data as data
from pathlib import Path

class AudioTranscriptionDataset(data.Dataset):
    def __init__(self, input_values, transcription):
        self.input_values = input_values
        self.transcription = transcription

    def __len__(self):
        return len(self.transcription)

    def __getitem__(self, index):
        return self.input_values[index], self.transcription[index]

dataset_path = Path('audio_transcription_dataset.pth')

if dataset_path.exists():
    dataset = torch.load(dataset_path)
    dataset.input_values = torch.cat([dataset.input_values, input_values], dim=0)
    dataset.transcription.extend(transcription)
else:
    dataset = AudioTranscriptionDataset(input_values, transcription)

torch.save(dataset, dataset_path)