from pytube import YouTube
from moviepy.editor import AudioFileClip
import os

def download_and_convert_to_mp3(youtube_url, start_time, end_time, output_path):
    yt = YouTube(youtube_url)
    audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
    downloaded_file = audio_stream.download(filename='temp_audio')

    audio_clip = AudioFileClip(downloaded_file).subclip(start_time, end_time)

    audio_clip.write_audiofile(output_path, codec='mp3', bitrate='320k')

    audio_clip.close()
    os.remove(downloaded_file)

    print(f"Audio successfully saved to {output_path}")

youtube_url = 'youtube url'
start_time = (0, 0)  # (minutes, seconds)
end_time = (1, 0)  # (minutes, seconds)

output_filename = input("Enter the output filename (with .mp3 extension): ")
output_path = f'D:/MyDoc/Music/{output_filename}'

download_and_convert_to_mp3(youtube_url, start_time, end_time, output_path)
