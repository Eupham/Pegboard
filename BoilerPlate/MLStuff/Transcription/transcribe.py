#transcribe.py
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch
import torchaudio
import torch.utils.data as data
from pathlib import Path

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
 
if __name__ == '__main__':
    # Initialize AudioTranscription object with the desired Wav2Vec2 model
    audio_transcription = AudioTranscription('facebook/wav2vec2-large-960h-lv60-self')

    # Transcribe an audio file and print the result
    transcription = audio_transcription.transcribe_audio('output.wav')
    print(transcription)