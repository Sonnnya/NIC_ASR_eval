import os
import audioread
import wave
from pydub import AudioSegment

def convert_mp3_to_wav_and_count_channels(directory):
    if not os.path.isdir(directory):
        print(f"Directory {directory} does not exist.")
        return

    files = os.listdir(directory)
    mp3_files = [f for f in files if f.endswith('.mp3')]
    wav_files = [f for f in files if f.endswith('.wav')]

    mono_count = 0
    stereo_count = 0

    for mp3_file in mp3_files:
        mp3_path = os.path.join(directory, mp3_file)
        wav_path = os.path.join(directory, mp3_file.replace('.mp3', '.wav'))

        audio = AudioSegment.from_file(mp3_path, format="mp3")
        audio.export(wav_path, format="wav")
        print(f"Converted {mp3_file} to {wav_path}")

        if audio.channels == 1:
            mono_count += 1
        elif audio.channels == 2:
            stereo_count += 1

    for wav_file in wav_files:
        wav_path = os.path.join(directory, wav_file)
        with wave.open(wav_path, 'rb') as wf:
            channels = wf.getnchannels()
            if channels == 1:
                mono_count += 1
            elif channels == 2:
                stereo_count += 1

    print(f"Number of mono files: {mono_count}")
    print(f"Number of stereo files: {stereo_count}")

target_directory = 'audio'
convert_mp3_to_wav_and_count_channels(target_directory)
