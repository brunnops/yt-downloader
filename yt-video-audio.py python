import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import time
import yt_dlp

# Caminho do FFmpeg (compatível com execução como .exe)
if getattr(sys, 'frozen', False):
    ffmpeg_path = os.path.join(sys._MEIPASS, "ffmpeg.exe")
else:
    ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg.exe")

pasta_destino = ""

def escolher_pasta():
    global pasta_destino
    pasta = filedialog.askdirectory()
    if pasta:
        pasta_destino = pasta
        label_pasta.config(text=f"Pasta selecionada:\n{pasta}", fg="green")

def baixar_audio():
    link = entrada_link.get().strip()

    if not link:
        messagebox.showwarning("Aviso", "Por favor, cole um link do YouTube.")
        return

    if not pasta_destino:
        messagebox.showwarning("Aviso", "Escolha uma pasta para salvar os arquivos.")
        return

    opcoes = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(pasta_destino, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': os.path.dirname(ffmpeg_path),
        'quiet': False
    }

    try:
        messagebox.showinfo("Iniciando", "Baixando áudio em MP3...")
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            info = ydl.extract_info(link, download=True)
            titulo = info.get("title", "audio")
            caminho_arquivo = os.path.join(pasta_destino, f"{titulo}.mp3")
            if os.path.exists(caminho_arquivo):
                agora = time.time()
                os.utime(caminho_arquivo, (agora, agora))
        messagebox.showinfo("Sucesso", "Download do áudio concluído com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao baixar: {e}")

def baixar_video():
    link = entrada_link.get().strip()

    if not link:
        messagebox.showwarning("Aviso", "Por favor, cole um link do YouTube.")
        return

    if not pasta_destino:
        messagebox.showwarning("Aviso", "Escolha uma pasta para salvar os arquivos.")
        return

    opcoes = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(pasta_destino, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'ffmpeg_location': os.path.dirname(ffmpeg_path),
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'quiet': False
    }

    try:
        messagebox.showinfo("Iniciando", "Baixando vídeo com áudio em MP4...")
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            info = ydl.extract_info(link, download=True)
            titulo = info.get("title", "video")
            caminho_arquivo = os.path.join(pasta_destino, f"{titulo}.mp4")
            if os.path.exists(caminho_arquivo):
                agora = time.time()
                os.utime(caminho_arquivo, (agora, agora))
        messagebox.showinfo("Sucesso", "Download do vídeo concluído com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao baixar: {e}")

janela = tk.Tk()
janela.title("YouTube Downloader")
janela.geometry("500x300")

label_link = tk.Label(janela, text="Cole o link do vídeo do YouTube:")
label_link.pack(pady=10)

entrada_link = tk.Entry(janela, width=60)
entrada_link.pack(pady=5)

botao_pasta = tk.Button(janela, text="Escolher pasta", command=escolher_pasta, bg="gray", fg="white")
botao_pasta.pack(pady=5)

label_pasta = tk.Label(janela, text="Nenhuma pasta selecionada.", fg="red")
label_pasta.pack()

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=20)

botao_baixar_mp3 = tk.Button(frame_botoes, text="Baixar Áudio (MP3)", command=baixar_audio, bg="green", fg="white", width=15)
botao_baixar_mp4 = tk.Button(frame_botoes, text="Baixar Vídeo (MP4)", command=baixar_video, bg="blue", fg="white", width=15)

botao_baixar_mp3.grid(row=0, column=0, padx=10)
botao_baixar_mp4.grid(row=0, column=1, padx=10)

janela.mainloop()
