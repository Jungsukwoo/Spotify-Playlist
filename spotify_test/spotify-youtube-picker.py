# app.py
from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

app = Flask(__name__)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope="playlist-modify-public playlist-modify-private"
))

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        query = request.form.get("track_name")
        if query:
            result = create_recommendation_playlist(query)
    return render_template("index.html", result=result)

def create_recommendation_playlist(query):
    try:
        search = sp.search(q=query, type="track", limit=1)
        if not search['tracks']['items']:
            return "❌ 해당 곡을 찾을 수 없습니다."

        track = search['tracks']['items'][0]
        track_id = track['id']
        track_name = track['name']
        artist_name = track['artists'][0]['name']

        recommendations = sp.recommendations(seed_tracks=[track_id], limit=20)
        track_ids = [t['id'] for t in recommendations['tracks']]

        user_id = sp.current_user()['id']
        playlist = sp.user_playlist_create(
            user=user_id,
            name=f"추천 - {track_name}",
            public=True
        )
        sp.playlist_add_items(playlist_id=playlist['id'], items=track_ids)

        return f"✅ <a href='{playlist['external_urls']['spotify']}' target='_blank'>플레이리스트 생성 완료</a>"

    except Exception as e:
        return f"❌ 에러 발생: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)