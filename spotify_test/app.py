# app.py
import os
from flask import Flask, request, render_template
from extract_mp3.youtube_to_mp3 import download_audio_from_youtube

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        url = request.form.get("yt_url")
        print(f"요청된 URL: {url}")
        if url:
            filename = download_audio_from_youtube(url)
            if filename:
                result = f"다운로드 완료: {filename}"
                
            else:
                result = "다운로드 실패"
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)