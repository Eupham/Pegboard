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