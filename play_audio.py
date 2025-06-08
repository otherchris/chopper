import simpleaudio as sa
import sys
import os
import wave
import time
from pynput import keyboard
from pydub import AudioSegment
import termios

def chop_sample(file_path):
    try:
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            return
        play_count = 0
        while True:
            play_count += 1
            print(f"Playing {file_path} (round {play_count})")
            wave_obj = sa.WaveObject.from_wave_file(file_path)
            play_obj = wave_obj.play()
            with wave.open(file_path, 'rb') as wf:
                audio_params = wf.getparams()
                duration = audio_params.nframes / audio_params.framerate
            start_time = time.time()
            markers = []
            def on_press(key):
                nonlocal markers
                try:
                    if key.char and key.char.lower() == 'c':
                        cur_time = time.time() - start_time
                        markers.append(cur_time)
                        prev_time = markers[-2] if len(markers) > 1 else 0
                        snippet_name = f"snip_{play_count}_{len(markers)}.wav"
                        with wave.open(file_path, 'rb') as r_wf:
                            # include 0.1s buffer before and after snippet boundaries
                            r_params = r_wf.getparams()
                            freq = r_params.framerate
                            total_frames = r_params.nframes
                            buffer_frames = int(0.1 * freq)
                            start_frame = int(prev_time * freq)
                            end_frame = int(cur_time * freq)
                            start_frame_adj = max(0, start_frame - buffer_frames)
                            end_frame_adj = min(total_frames, end_frame + buffer_frames)
                            r_wf.setpos(start_frame_adj)
                            frames_to_read = end_frame_adj - start_frame_adj
                            frames = r_wf.readframes(frames_to_read)
                        with wave.open(snippet_name, 'wb') as w_wf:
                            w_wf.setparams(r_params)
                            w_wf.writeframes(frames)
                        print(f"\nSnippet saved: {snippet_name}")
                except AttributeError:
                    pass
            listener = keyboard.Listener(on_press=on_press)
            listener.start()
            bar_length = 50
            while play_obj.is_playing():
                elapsed = time.time() - start_time
                percent = min(elapsed / duration, 1.0)
                filled = int(bar_length * percent)
                bar = '#' * filled + '-' * (bar_length - filled)
                sys.stdout.write(f"\rPlaying: |{bar}| {int(percent*100)}% (press 'c' to capture)")
                sys.stdout.flush()
                time.sleep(0.1)
            sys.stdout.write("\n")
            listener.stop()
            termios.tcflush(sys.stdin, termios.TCIFLUSH)
            print(f"Finished playing: {file_path} (round {play_count})")
            play_again = input("Play again? (y/N): ").strip().lower()
            if play_again != 'y':
                print(f"xxx{play_again}xxx")
                break
    except Exception as e:
        print(f"Error playing audio file: {str(e)}")
    # After chopping session, review saved snippets
    snippet_files = [f for f in os.listdir('.') if f.startswith('snip_') and f.endswith('.wav')]
    for snippet in snippet_files:
        print(f"Review snippet: {snippet}")
        wave_obj = sa.WaveObject.from_wave_file(snippet)
        play_obj = wave_obj.play()
        play_obj.wait_done()
        keep = input("Keep snippet? (y/N): ").strip().lower() == 'y'
        if not keep:
            os.remove(snippet)
            print(f"Deleted snippet: {snippet}")
    print("Snippet review complete.")

def convert_mp3_to_wav(mp3_path):
    wav_path = os.path.splitext(mp3_path)[0] + '.wav'
    try:
        audio = AudioSegment.from_mp3(mp3_path)
        audio.export(wav_path, format='wav')
        print(f"Converted {mp3_path} to {wav_path}")
        return wav_path
    except Exception as e:
        print(f"Error converting MP3 to WAV: {e}")
        return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python play_audio.py <path_to_audio_file>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    if audio_file.lower().endswith('.mp3'):
        converted = convert_mp3_to_wav(audio_file)
        if converted:
            audio_file = converted

    chop_sample(audio_file)

if __name__ == "__main__":
    main()
