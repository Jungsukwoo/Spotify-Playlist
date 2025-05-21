from flask import Blueprint, render_template, request
from app.utils.spotify_auth import get_spotify_access_token
import requests

recommendation_views = Blueprint("recommendation_views", __name__)

SPOTIFY_RECOMMEND_URL = "https://api.spotify.com/v1/recommendations"
SPOTIFY_SEARCH_URL = "https://api.spotify.com/v1/search"
SPOTIFY_AUDIO_FEATURES_URL = "https://api.spotify.com/v1/audio-features"


@recommendation_views.route("/recommend", methods=["GET", "POST"])
def recommend():
    access_token = get_spotify_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    recommendations = []
    genres = get_available_genres(headers)

    if request.method == "POST":
        track_name = request.form.get("track_name")
        artist_name = request.form.get("artist_name")
        selected_genres = request.form.getlist("genres")

        seed_tracks = get_track_id(track_name, headers)
        seed_artists = get_artist_id(artist_name, headers)

        params = {
            "limit": 20,
            "seed_tracks": seed_tracks,
            "seed_artists": seed_artists,
            "seed_genres": ",".join(selected_genres)
        }

        resp = requests.get(SPOTIFY_RECOMMEND_URL, headers=headers, params=params)
        data = resp.json()
        for item in data.get("tracks", []):
            recommendations.append({
                "name": item["name"],
                "artist": item["artists"][0]["name"]
            })

    return render_template("recommendation.html", genres=genres, recommendations=recommendations)

def get_available_genres(headers):
    resp = requests.get("https://api.spotify.com/v1/recommendations/available-genre-seeds", headers=headers)
    return resp.json().get("genres", [])

def get_track_id(track_name, headers):
    params = {"q": track_name, "type": "track", "limit": 1}
    resp = requests.get(SPOTIFY_SEARCH_URL, headers=headers, params=params)
    items = resp.json().get("tracks", {}).get("items", [])
    return items[0]["id"] if items else ""

def get_artist_id(artist_name, headers):
    params = {"q": artist_name, "type": "artist", "limit": 1}
    resp = requests.get(SPOTIFY_SEARCH_URL, headers=headers, params=params)
    items = resp.json().get("artists", {}).get("items", [])
    return items[0]["id"] if items else ""