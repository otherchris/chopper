"""
Top-level CLI that prompts the user for the project name.
"""
import os
import sys
import argparse
import sounddevice as sd
from record_snippets import record_input_snippets
from play_audio import chop_sample, convert_mp3_to_wav, review_wav_files

def main():
    parser = argparse.ArgumentParser(description='CLI for recording or chopping audio snippets')
    parser.add_argument('-f', '--file', dest='file_path', help='Path to audio file')
    parser.add_argument('-r', '--remove', action='store_true', dest='remove', help='Preview and delete .wav files in a directory')
    args = parser.parse_args()
    file_path = args.file_path
    if args.remove:
        if not file_path:
            print("Error: Directory path must be provided with -f when using -r flag.")
            parser.print_usage()
            sys.exit(1)
        if not os.path.isdir(file_path):
            print(f"Error: '{file_path}' is not a directory.")
            sys.exit(1)
        wav_paths = [os.path.join(file_path, f) for f in os.listdir(file_path) if f.lower().endswith('.wav')]
        if not wav_paths:
            print("No .wav files found in the directory.")
            sys.exit(0)
        review_wav_files(wav_paths)
        sys.exit(0)
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
