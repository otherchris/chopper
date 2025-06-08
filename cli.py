"""
Top-level CLI that prompts the user for the project name.
"""
import os
import sys
import argparse
import sounddevice as sd
from record_snippets import record_input_snippets
from play_audio import chop_sample, convert_mp3_to_wav

def main():
    parser = argparse.ArgumentParser(description='CLI for recording or chopping audio snippets')
    parser.add_argument('-f', '--file', dest='file_path', help='Path to audio file')
    args = parser.parse_args()
    file_path = args.file_path
    project_name = input("Enter the name of the project: ")
    if os.path.exists(project_name):
        print(f"Error: Directory '{project_name}' already exists.")
        sys.exit(1)
    print(f"Project name set to: {project_name}")
    if file_path:
        print(f"Using audio file: {file_path}")
        os.makedirs(project_name)
        print(f"Created directory: {project_name}")
        os.chdir(project_name)
        if file_path.lower().endswith('.mp3'):
            wav_path = convert_mp3_to_wav(file_path)
            if wav_path:
                file_path = wav_path
            else:
                sys.exit(1)
        chop_sample(file_path)
    else:
        devices = sd.query_devices()
        input_devices = [(i, dev) for i, dev in enumerate(devices) if dev['max_input_channels'] > 0]
        print("Available input devices:")
        for i, dev in input_devices:
            print(f"{i}: {dev['name']} (max channels: {dev['max_input_channels']})")
        while True:
            selection = input("Enter device ID: ")
            try:
                device = int(selection)
                if any(i == device for i, _ in input_devices):
                    break
                else:
                    print("Invalid device ID.")
            except ValueError:
                print("Please enter a valid integer.")
        print(f"Using device ID: {device}")
        os.makedirs(project_name)
        print(f"Created directory: {project_name}")
        os.chdir(project_name)
        record_input_snippets(device=device)

if __name__ == "__main__":
    main()
