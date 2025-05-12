import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException

# .env 파일에서 환경변수 불러오기
load_dotenv()

# Spotify 인증
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-read-private"
))

# 1. 곡 검색
query = "Levitating Dua Lipa"
print(f"\n🔍 검색어: {query}")
search_result = sp.search(q=query, type="track", limit=1)

if not search_result['tracks']['items']:
    print("❌ 곡을 찾을 수 없습니다.")
    exit()

track = search_result['tracks']['items'][0]
track_id = track['id']
track_name = track['name']
track_artist = track['artists'][0]['name']
print(f"\n🎵 기준 곡: {track_name} - {track_artist}")
print(f"🎯 track_id: {track_id}")

# 2. 추천 곡 요청 (예외처리 포함)
try:
    recommendations = sp.recommendations(seed_tracks=[track_id], limit=20)
    if not recommendations['tracks']:
        print("❌ 추천 결과가 없습니다. 다른 곡으로 시도해보세요.")
        exit()
except SpotifyException as e:
    print("\n❌ 추천 곡 요청 실패!")
    print(e)
    exit()

# 3. 추천 곡 리스트 출력 및 저장
print("\n🎧 추천 곡 리스트:")
recommended_songs = []

for i, rec in enumerate(recommendations['tracks'], start=1):
    name = rec['name']
    artist = rec['artists'][0]['name']
    print(f"{i}. {name} - {artist}")
    recommended_songs.append(f"{name} {artist}")

# 🎯 추천 곡 리스트 후속 작업용 저장 확인
# print(recommended_songs)  # 예: ['Song1 Artist1', 'Song2 Artist2', ...]