import tkinter as tk
from tkinter import filedialog, messagebox
from pytube import YouTube
from moviepy.editor import AudioFileClip
import os

def download_and_convert_to_mp3(youtube_url, start_time, end_time, output_path, full_video):
    try:
        yt = YouTube(youtube_url)
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        if audio_stream:
            downloaded_file = audio_stream.download(filename='temp_audio')
        else:
            raise ValueError("No audio stream available for download.")

        if full_video:
            audio_clip = AudioFileClip(downloaded_file)
        else:
            audio_clip = AudioFileClip(downloaded_file).subclip(start_time, end_time)

        if audio_clip:
            audio_clip.write_audiofile(output_path, codec='mp3', bitrate='320k')
            audio_clip.close()
            os.remove(downloaded_file)
            messagebox.showinfo("Success", f"Audio successfully saved to {output_path}")
        else:
            raise ValueError("Failed to create AudioFileClip from downloaded file.")
    except KeyError as e:
        if "get_throttling_function_name" in str(e):
            messagebox.showerror("Error", "An error occurred: YouTube has changed its site layout. Please try again later or update pytube.")
        else:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def convert():
    youtube_url = url_entry.get()
    output_filename = output_name_entry.get()

    if not youtube_url or not output_filename:
        messagebox.showerror("Input Error", "Please provide both YouTube URL and Output Filename.")
        return

    try:
        if full_video_var.get():
            start_time = None
            end_time = None
        else:
            start_time = (int(start_min_entry.get()), int(start_sec_entry.get()))
            end_time = (int(end_min_entry.get()), int(end_sec_entry.get()))

        output_path = f'{filedialog.askdirectory()}/{output_filename}.mp3'
        download_and_convert_to_mp3(youtube_url, start_time, end_time, output_path, full_video_var.get())
    except ValueError:
        messagebox.showerror("Input Error", "Invalid time format. Please enter integers for minutes and seconds.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("YouTube to MP3 Converter")

tk.Label(root, text="YouTube URL:").grid(row=0, column=0, padx=10, pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Start Time (min:sec):").grid(row=1, column=0, padx=10, pady=10)
start_min_entry = tk.Entry(root, width=5)
start_min_entry.grid(row=1, column=1, padx=(10, 0), pady=10, sticky='W')
start_sec_entry = tk.Entry(root, width=5)
start_sec_entry.grid(row=1, column=1, padx=(70, 10), pady=10, sticky='W')

tk.Label(root, text="End Time (min:sec):").grid(row=2, column=0, padx=10, pady=10)
end_min_entry = tk.Entry(root, width=5)
end_min_entry.grid(row=2, column=1, padx=(10, 0), pady=10, sticky='W')
end_sec_entry = tk.Entry(root, width=5)
end_sec_entry.grid(row=2, column=1, padx=(70, 10), pady=10, sticky='W')

tk.Label(root, text="Output Filename (.mp3):").grid(row=3, column=0, padx=10, pady=10)
output_name_entry = tk.Entry(root, width=50)
output_name_entry.grid(row=3, column=1, padx=10, pady=10)

full_video_var = tk.BooleanVar()
full_video_check = tk.Checkbutton(root, text="Convert Full Video", variable=full_video_var)
full_video_check.grid(row=4, column=0, columnspan=2, pady=10)

convert_button = tk.Button(root, text="Convert", command=convert)
convert_button.grid(row=5, column=0, columnspan=2, pady=20)

root.mainloop()
