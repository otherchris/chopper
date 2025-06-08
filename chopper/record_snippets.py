import sounddevice as sd
import soundfile as sf
from pynput import keyboard

def record_input_snippets(device=None, samplerate=None, channels=None):
    """
    Record audio from the input device and create WAV snippets on 'c' key presses.
    Press 'c' to start/stop each snippet, 'q' to quit.
    """
    snippet_counter = 0
    recording_flag = False
    writer = None

    def audio_callback(indata, frames, time_info, status):
        nonlocal writer, recording_flag
        if recording_flag and writer is not None:
            writer.write(indata)

    def on_press(key):
        nonlocal snippet_counter, recording_flag, writer
        try:
            if key.char.lower() == 'c':
                if not recording_flag:
                    snippet_counter += 1
                    fname = f"snippet_{snippet_counter}.wav"
                    writer = sf.SoundFile(fname, mode='w', samplerate=samplerate, channels=channels or indata.shape[1], subtype='PCM_16')
                    recording_flag = True
                    print(f"Started snippet {snippet_counter} -> {fname}")
                else:
                    recording_flag = False
                    writer.close()
                    writer = None
                    print(f"Finished snippet {snippet_counter}")
            elif key.char.lower() == 'q':
                print("Quitting...")
                if recording_flag and writer:
                    writer.close()
                return False
        except AttributeError:
            pass

    # Determine parameters
    default_dev = sd.default.device[0]
    device = device if device is not None else default_dev
    samplerate = samplerate or int(sd.query_devices(device, 'input')['default_samplerate'])
    channels = channels or sd.query_devices(device, 'input')['max_input_channels']

    print("Press 'c' to start/stop snippet, 'q' to quit.")
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    with sd.InputStream(device=device, samplerate=samplerate, channels=channels, callback=audio_callback):
        listener.join()

    print("Recording session ended.")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Record live audio snippets from input device.')
    parser.add_argument('--device', type=int, help='Input device ID')
    parser.add_argument('--samplerate', type=int, help='Sampling rate')
    parser.add_argument('--channels', type=int, help='Number of channels')
    args = parser.parse_args()
    device = args.device
    # If no device provided, list and prompt
    if device is None:
        devices = sd.query_devices()
        input_devices = [(idx, dev) for idx, dev in enumerate(devices) if dev['max_input_channels'] > 0]
        print("Available input devices:")
        for idx, dev in input_devices:
            print(f"{idx}: {dev['name']} (Max Input Channels: {dev['max_input_channels']})")
        while True:
            selection = input("Select device ID: ")
            try:
                sel = int(selection)
                if any(idx == sel for idx, _ in input_devices):
                    device = sel
                    break
                else:
                    print("Invalid selection, try again.")
            except ValueError:
                print("Please enter a valid integer.")
    record_input_snippets(device=device, samplerate=args.samplerate, channels=args.channels)
