# app/views/main_views.py

from flask import Blueprint, render_template, request
from app.utils.spotify_auth import get_spotify_access_token
import requests

main_views = Blueprint("main_views", __name__)

SPOTIFY_GENRE_URL = "https://api.spotify.com/v1/recommendations/available-genre-seeds"

@main_views.route("/", methods=["GET", "POST"])
def main_page():
    access_token = get_spotify_access_token()
    if not access_token:
        return render_template("MainPage.html", error="Spotify 인증 실패", genres=[])

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Spotify에서 장르 목록 받아오기
    genre_resp = requests.get(SPOTIFY_GENRE_URL, headers=headers)
    if genre_resp.status_code != 200:
        print("🔴 장르 가져오기 실패:", genre_resp.status_code, genre_resp.text)
        return render_template("MainPage.html", error="장르 로드 실패", genres=[])

    genres = genre_resp.json().get("genres", [])
    return render_template("MainPage.html", genres=genres)