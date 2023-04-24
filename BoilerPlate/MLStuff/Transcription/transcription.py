from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch
import torchaudio

# load model and processor
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h-lv60-self", from_tf=False)

audio_file = "output.wav"
waveform, sample_rate = torchaudio.load(audio_file)

# Resample the audio to 16kHz
resampler = torchaudio.transforms.Resample(sample_rate, 16000)
waveform = resampler(waveform)

# Convert the waveform to a tensor and normalize it
input_values = waveform.squeeze().to(torch.float32)
input_values /= torch.max(torch.abs(input_values))

# Pass the entire waveform to the model
logits = model(input_values.unsqueeze(0)).logits

# take argmax and decode# Save the dataset to a file
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

# Define the file path for the dataset
dataset_path = Path('audio_transcription_dataset.pth')

# Check if the file exists
if dataset_path.exists():
    # Load the dataset from the file
    dataset = torch.load(dataset_path)
    # Add the new data to the existing dataset
    dataset.input_values = torch.cat([dataset.input_values, input_values], dim=0)
    dataset.transcription.extend(transcription)
else:
    # Create the dataset if the file doesn't exist
    dataset = AudioTranscriptionDataset(input_values, transcription)

# Save the dataset back to the file
torch.save(dataset, dataset_path)