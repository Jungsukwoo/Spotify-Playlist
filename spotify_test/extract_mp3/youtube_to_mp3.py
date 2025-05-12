# extract_mp3/youtube_to_mp3.py
import os
from pytubefix import YouTube

def download_audio_from_youtube(url: str) -> str:
    try:
        yt = YouTube(url)
        print(f"영상 찾는 중: {yt.title}")

        audio_stream = yt.streams.filter(only_audio=True).first()
        if audio_stream is None:
            raise Exception("오디오 스트림을 찾을 수 없습니다.")

        output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "downloads"))
        os.makedirs(output_path, exist_ok=True)

        print("오디오 다운로드 중...")
        downloaded_file = audio_stream.download(output_path=output_path)

        base, _ = os.path.splitext(downloaded_file)
        mp3_file = base + ".mp3"
        os.rename(downloaded_file, mp3_file)

        print(f"다운로드 완료: {mp3_file}")
        return os.path.basename(mp3_file)

    except Exception as e:
        print(f"오류 발생: {e}")
        return ""