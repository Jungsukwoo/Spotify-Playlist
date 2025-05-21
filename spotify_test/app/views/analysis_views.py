# app/views/analysis_views.py

import os
import requests
from flask import Blueprint, render_template, request
from dotenv import load_dotenv
from app.utils.spotify_auth import get_spotify_access_token

load_dotenv()

analysis_views = Blueprint("analysis_views", __name__)

SPOTIFY_SEARCH_URL = "https://api.spotify.com/v1/search"
SPOTIFY_AUDIO_FEATURES_URL = "https://api.spotify.com/v1/audio-features"


def get_spotify_access_token():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    auth_response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
    )

    if auth_response.status_code == 200:
        return auth_response.json().get("access_token")
    else:
        print("Token 요청 실패:", auth_response.status_code, auth_response.text)
        return None


@analysis_views.route("/analysis", methods=["GET", "POST"])
def analysis_page():
    if request.method == "POST":
        track_query = request.form.get("track_query")
        if not track_query:
            return render_template("analysis.html", error="검색어를 입력하십시오.")

        try:
            access_token = get_spotify_access_token()
            if not access_token:
                return render_template("analysis.html", error="Spotify 인증 실패")

            headers = {
                "Authorization": f"Bearer {access_token}"
            }

            # Step 1: 트랙 검색
            search_params = {
                "q": track_query,
                "type": "track",
                "limit": 1
            }
            resp = requests.get(SPOTIFY_SEARCH_URL, headers=headers, params=search_params)
            print(resp.status_code)
            print(resp.json())
            
            data = resp.json()

            items = data.get("tracks", {}).get("items", [])
            if not items:
                return render_template("analysis.html", error="검색 결과가 없습니다.")

            track = items[0]
            track_id = track["id"]
            track_info = {
                "title": track["name"],
                "artist": track["artists"][0]["name"],
                "album": track["album"]["name"],
                "release_date": track["album"]["release_date"],
                "explicit": track["explicit"]
            }

            # Step 2: 오디오 피처 추출
            feat_resp = requests.get(f"{SPOTIFY_AUDIO_FEATURES_URL}/{track_id}", headers=headers)           
            feat = feat_resp.json()
            audio_features = {
                "bpm": feat.get("tempo"),
                "key": feat.get("key"),
                "mode": feat.get("mode"),
                "camelot": convert_to_camelot(feat.get("key"), feat.get("mode"))
            }

            return render_template("analysis.html", track_info=track_info, audio_features=audio_features)

        except Exception as e:
            return render_template("analysis.html", error="서버가 불안정합니다. 잠시 뒤 재시도 하십시오.")

    return render_template("analysis.html")


def convert_to_camelot(key, mode):
    camelot_map = {
        0: "8B" if mode == 1 else "8A",
        1: "3B" if mode == 1 else "3A",
        2: "10B" if mode == 1 else "10A",
        3: "5B" if mode == 1 else "5A",
        4: "12B" if mode == 1 else "12A",
        5: "7B" if mode == 1 else "7A",
        6: "2B" if mode == 1 else "2A",
        7: "9B" if mode == 1 else "9A",
        8: "4B" if mode == 1 else "4A",
        9: "11B" if mode == 1 else "11A",
        10: "6B" if mode == 1 else "6A",
        11: "1B" if mode == 1 else "1A"
    }
    return camelot_map.get(key, "N/A")