# Chopper CLI Tool

### Hey this is some tossed together unsupervised vibe code so do not expect it to work predictably. Files seem to work ok, the live recording mode _works_ but it's not really _right_.

Chopper is a command-line utility for recording or chopping audio snippets from live input devices or existing audio files.

## Features

- **Live recording mode**: Capture audio snippets in real time by pressing `c` to start/stop each clip.
- **File chopping mode**: Slice existing audio files (.wav or .mp3) by marking snippet boundaries during playback.
- **Interactive snippet review**: Play back and choose which snippets to keep or delete.

## Installation

pipx install git+https://github.com/otherchris/chopper.git
```

> Requires Python 3.6+ and system audio devices.

## Usage

### Top-level CLI

```bash
python3 cli.py [-f /path/to/audio.mp3|.wav]
```

- `-f, --file <file_path>`: Path to an existing audio file. If omitted, enters live recording mode.

**Workflow**:
1. **Project name**: Enter a name; a new directory with that name will be created.
2. **Mode selection**:
   - **File mode**: Converts MP3 to WAV (if needed), then plays back audio. Press `c` during playback to mark snippet boundaries. After playback, you'll review and confirm snippets.
   - **Live mode**: Lists input devices; enter device ID. Press `c` to start/stop each snippet, `q` to quit.
3. **Review**: After recording or chopping, play each saved snippet and choose to keep (y) or delete (N).

All snippets are saved in the project folder.

### Standalone Scripts

- **Record live snippets**:
  ```bash
  python3 record_snippets.py [--device ID] [--samplerate RATE] [--channels N]
  ```
  Press `c` to toggle recording a snippet, `q` to quit.

- **Chop an audio file**:
  ```bash
  python3 play_audio.py /path/to/file.wav
  ```
  During playback, press `c` to capture snippets.

- **List audio devices**:
  ```bash
  python3 audio_devices.py
  ```

## Snippet Naming

- **Live mode**: `snippet_1.wav`, `snippet_2.wav`, …
- **File mode**: `snip_<round>_<index>.wav` (e.g., `snip_1_1.wav`).

## Dependencies

- pydub
- simpleaudio
- pynput
- sounddevice
- soundfile

> All versions are specified in `requirements.txt`.

## System Requirements

- **ffmpeg**: Installed and available in PATH for MP3→WAV conversion via pydub.
- **PortAudio**: Required by sounddevice.
- **libsndfile**: Required by soundfile.

## License

License, that's funny.
