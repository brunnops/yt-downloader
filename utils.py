# utils.py
from pytube import YouTube
import os

def baixar_video(url, tipo='audio'):
    yt = YouTube(url)

    if tipo == 'audio':
        stream = yt.streams.filter(only_audio=True).first()
        out_file = stream.download(output_path="downloads")
        base, _ = os.path.splitext(out_file)
        mp3_file = base + '.mp3'
        os.rename(out_file, mp3_file)
        return mp3_file

    elif tipo == 'video':
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        mp4_file = stream.download(output_path="downloads")
        return mp4_file
