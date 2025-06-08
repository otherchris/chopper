import sounddevice as sd

def list_output_devices():
    """
    Print a list of available audio output devices on the system.
    """
    devices = sd.query_devices()
    print("Available audio output devices:")
    for idx, dev in enumerate(devices):
        if dev['max_output_channels'] > 0:
            print(f"{idx}: {dev['name']} (Max Output Channels: {dev['max_output_channels']})")

def list_input_devices():
    """
    Print a list of available audio input devices on the system.
    """
    devices = sd.query_devices()
    print("Available audio input devices:")
    for idx, dev in enumerate(devices):
        if dev['max_input_channels'] > 0:
            print(f"{idx}: {dev['name']} (Max Input Channels: {dev['max_input_channels']})")
