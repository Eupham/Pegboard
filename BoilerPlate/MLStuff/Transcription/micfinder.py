import pyaudio

p = pyaudio.PyAudio()

device_index = None
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    if info['maxInputChannels'] > 0:
        print(f"Device {i} has {info['maxInputChannels']} input channels.")
        device_index = i
        break

if device_index is None:
    print("Error: No input device found.")
else:
    print(f"Using device {device_index} for recording.")