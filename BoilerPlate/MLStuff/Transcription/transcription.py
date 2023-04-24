from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch
import torchaudio

# load model and processor
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")

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

# take argmax and decode
predicted_ids = torch.argmax(logits, dim=-1)
transcription = processor.decode(predicted_ids[0])
print(transcription)