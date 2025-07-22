import os
from flask import Flask, request, render_template, send_file
import yt_dlp
import glob

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    mensagem = ""
    if request.method == 'POST':
        url = request.form.get('url')
        formato = request.form.get('formato', 'mp3')

        # Apaga arquivos antigos
        for f in glob.glob("download.*"):
            os.remove(f)

        if not url:
            mensagem = "URL inválida."
        else:
            try:
                saida = 'download.%(ext)s'
                ydl_opts = {
                    'format': 'bestaudio/best' if formato == 'mp3' else 'bestvideo+bestaudio/best',
                    'outtmpl': saida,
                    'merge_output_format': 'mp4' if formato == 'mp4' else None,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }] if formato == 'mp3' else [],
                    'quiet': True,
                    'no_warnings': True
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

                nome_arquivo = [f for f in os.listdir() if f.startswith('download.')][0]
                return send_file(nome_arquivo, as_attachment=True)
            except Exception as e:
                mensagem = f"Erro ao baixar: {str(e)}"

    return render_template('index.html', mensagem=mensagem)
