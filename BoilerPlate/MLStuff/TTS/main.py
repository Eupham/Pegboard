import torchaudio
import torch
from speechbrain.pretrained import Tacotron2
from speechbrain.pretrained import HIFIGAN

# Intialize TTS (tacotron2) and Vocoder (HiFIGAN)
tacotron2 = Tacotron2.from_hparams(source="speechbrain/tts-tacotron2-ljspeech", savedir="tmpdir_tts")
hifi_gan = HIFIGAN.from_hparams(source="speechbrain/tts-hifigan-ljspeech", savedir="tmpdir_vocoder")

# Running the TTS
mel_output, mel_length, alignment = tacotron2.encode_text("Mary had a little lamb")

# Running Vocoder (spectrogram-to-waveform)
waveforms = hifi_gan.decode_batch(mel_output)

# Apply pitch shifting by a factor of -100 cents (i.e., one semitone down)
waveform_pitch_shifted = torchaudio.functional.pitch_shift(waveforms.squeeze(1), 22050, n_steps=-2)

# Save the pitch-shifted waveform
torchaudio.save('example_TTS_pitch_shifted.wav', waveform_pitch_shifted, 22050)
