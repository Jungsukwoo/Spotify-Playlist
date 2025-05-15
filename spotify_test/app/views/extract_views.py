from flask import Blueprint, render_template, request
from pytubefix import YouTube
from extract_mp3.youtube_to_mp3 import download_audio_from_youtube
from pytubefix.exceptions import RegexMatchError

extract_views = Blueprint('extract_views', __name__)

@extract_views.route('/extract', methods=['GET', 'POST'])
def extract_audio():
    video_url = None
    thumbnail_url = None
    title = None
    alert_message = None

    if request.method == 'POST':
        url = request.form.get("yt_url", "").strip()

        if not url:
            alert_message = "URL을 입력하십시오."
        else:
            try:
                yt = YouTube(url)
                video_url = url
                thumbnail_url = yt.thumbnail_url
                title = yt.title
            except RegexMatchError:
                alert_message = "URL을 재확인하십시오."
            except Exception:
                alert_message = "서버가 불안정합니다. 잠시 뒤 재시도 하십시오."

    return render_template(
        "index.html",
        video_url=video_url,
        thumbnail_url=thumbnail_url,
        title=title,
        alert_message=alert_message
    )

@extract_views.route('/extract/download', methods=['POST'])
def download():
    url = request.form.get("yt_url", "").strip()
    video_url = url
    title = None
    thumbnail_url = None
    alert_message = None

    if not url:
        alert_message = "URL이 비어있습니다."
    else:
        try:
            yt = YouTube(url)
            title = yt.title
            thumbnail_url = yt.thumbnail_url
            filename = download_audio_from_youtube(url)
            alert_message = f"✅ 다운로드 완료: {filename}"
        except Exception:
            alert_message = "❌ 다운로드 실패: 서버가 불안정합니다."

    return render_template(
        "index.html",
        video_url=video_url,
        thumbnail_url=thumbnail_url,
        title=title,
        alert_message=alert_message
    )