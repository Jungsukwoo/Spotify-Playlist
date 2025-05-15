from flask import Blueprint, render_template, request
from extract_mp3.youtube_to_mp3 import download_audio_from_youtube

app_views = Blueprint('app_views', __name__)

@app_views.route("/")
def main_page():
    return render_template("MainPage.html")

@app_views.route("/extract", methods=["GET", "POST"])
def extract_audio():
    result = None
    if request.method == "POST":
        url = request.form.get("yt_url")
        if url:
            filename = download_audio_from_youtube(url)
            result = f"다운로드 완료: {filename}" if filename else "다운로드 실패"
    return render_template("index.html", result=result)