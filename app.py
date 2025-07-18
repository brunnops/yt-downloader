from flask import after_this_request

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data.get("url")
    tipo = data.get("tipo")  # 'audio' ou 'video'

    if not url or tipo not in ["audio", "video"]:
        return jsonify({"error": "URL ou tipo de download inválido."}), 400

    filename = f"{uuid.uuid4()}.%(ext)s"
    filepath_template = os.path.join(download_folder, filename)

    if tipo == "audio":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": filepath_template,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }
    else:  # tipo == "video"
        ydl_opts = {
            "format": "best",
            "outtmpl": filepath_template,
        }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            final_path = ydl.prepare_filename(info_dict)
            if tipo == "audio":
                final_path = os.path.splitext(final_path)[0] + ".mp3"

            @after_this_request
            def cleanup(response):
                try:
                    os.remove(final_path)
                except Exception as e:
                    print(f"Erro ao deletar arquivo: {e}")
                return response

            return send_file(final_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
