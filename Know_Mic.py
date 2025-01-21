import pyaudio

def get_active_microphone():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')

    for i in range(num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        if device_info.get('maxInputChannels') > 0 and device_info.get('hostApi') == info.get('index'):
            if device_info.get('index') == p.get_default_input_device_info().get('index'):
                return device_info.get('name')
    return None

# Main program
if __name__ == "__main__":
    active_microphone = get_active_microphone()
    if active_microphone:
        print("Active Microphone:", active_microphone)
    else:
        print("No active microphone found.")