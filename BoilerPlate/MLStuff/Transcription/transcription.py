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