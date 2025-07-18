import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from yt_dlp import YoutubeDL
import threading
import os
import time

def baixar_audio():
    url = entrada_url.get()
    if not url:
        messagebox.showwarning("Aviso", "Por favor, insira a URL do vídeo.")
        return

    pasta_destino = filedialog.askdirectory()
    if not pasta_destino:
        return

    btn_audio.config(state=tk.DISABLED)
    btn_video.config(state=tk.DISABLED)
    progresso.grid(row=4, column=0, columnspan=2, padx=10, pady=(0,10))  # Mostrar barra de progresso
    progresso["value"] = 0
    progresso["maximum"] = 100

    def tarefa():
        opcoes = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(pasta_destino, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'progress_hooks': [atualizar_progresso],
            'ffmpeg_location': 'ffmpeg.exe'
        }

        with YoutubeDL(opcoes) as ydl:
            info = ydl.extract_info(url)
            caminho_arquivo = info.get('_filename')  # Corrigido
            time.sleep(0.5)
            os.utime(caminho_arquivo, None)

        messagebox.showinfo("Concluído", "Áudio baixado com sucesso!")
        resetar_interface()

    threading.Thread(target=tarefa).start()

def baixar_video():
    url = entrada_url.get()
    if not url:
        messagebox.showwarning("Aviso", "Por favor, insira a URL do vídeo.")
        return

    pasta_destino = filedialog.askdirectory()
    if not pasta_destino:
        return

    btn_audio.config(state=tk.DISABLED)
    btn_video.config(state=tk.DISABLED)
    progresso.grid(row=4, column=0, columnspan=2, padx=10, pady=(0,10))  # Mostrar barra de progresso
    progresso["value"] = 0
    progresso["maximum"] = 100

    def tarefa():
        opcoes = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(pasta_destino, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'progress_hooks': [atualizar_progresso],
            'ffmpeg_location': 'ffmpeg.exe'
        }

        with YoutubeDL(opcoes) as ydl:
            info = ydl.extract_info(url)
            caminho_arquivo = info.get('_filename')  # Corrigido
            time.sleep(0.5)
            os.utime(caminho_arquivo, None)

        messagebox.showinfo("Concluído", "Vídeo baixado com sucesso!")
        resetar_interface()

    threading.Thread(target=tarefa).start()

def atualizar_progresso(d):
    if d['status'] == 'downloading':
        if 'total_bytes' in d and d.get('downloaded_bytes'):
            progresso_total = d['total_bytes']
            progresso_atual = d['downloaded_bytes']
            percentual = (progresso_atual / progresso_total) * 100
            progresso["value"] = percentual
            root.update_idletasks()
    elif d['status'] == 'finished':
        progresso["value"] = 100

def resetar_interface():
    btn_audio.config(state=tk.NORMAL)
    btn_video.config(state=tk.NORMAL)
    progresso.grid_remove()

# Interface
root = tk.Tk()
root.title("YouTube Downloader")
root.resizable(False, False)

tk.Label(root, text="URL do vídeo:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
entrada_url = tk.Entry(root, width=50)
entrada_url.grid(row=0, column=1, padx=10, pady=10)

btn_audio = tk.Button(root, text="Baixar Áudio (MP3)", command=baixar_audio)
btn_audio.grid(row=1, column=0, padx=10, pady=10)

btn_video = tk.Button(root, text="Baixar Vídeo (MP4)", command=baixar_video)
btn_video.grid(row=1, column=1, padx=10, pady=10)

progresso = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progresso.grid_remove()  # Começa escondido

root.mainloop()
