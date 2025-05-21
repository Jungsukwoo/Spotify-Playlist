import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_spotify_access_token():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("🔴 SPOTIFY_CLIENT_ID 또는 SECRET이 .env에 없습니다.")
        return None

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
    )

    if response.status_code == 200:
        print("🟢 Spotify 인증 성공")
        return response.json().get("access_token")
    else:
        print("🔴 Spotify 인증 실패:", response.status_code, response.text)
        return None