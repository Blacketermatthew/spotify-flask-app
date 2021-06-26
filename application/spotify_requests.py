import os
from dotenv import load_dotenv
import requests
import json
import psycopg2
import spotipy  # module for interacting with Spotify
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy.util as util
from datetime import datetime


########## SCOPES ###########
# You have to specify what you'd like to access through pre-defined scopes.
# LIST OF AVAILABLE SCOPES: https://developer.spotify.com/documentation/general/guides/scopes/#user-read-playback-state
# user-top-read: Read access to a user's top artists and tracks.
# playlist-modify-private: Write access to your private playlists
# playlist-modify-public: Same, but for public playlists.


######### VARIABLES #########

## Traditional variables from .env
load_dotenv()

# Used to configure the app when it's deployed to Heroku
if os.environ.get("IS_HEROKU"):
    print("HEROKU")
    client_id = os.environ.get("SPOTIPY_CLIENT_ID")
    client_secret = os.environ.get("SPOITPY_CLIENT_SECRET")
    discover_playlist_uri = os.environ.get("DISCOVER_WEEKLY_PLAYLIST")
    starred_playlist_uri = os.environ.get("STARRED_PLAYLIST")
    run_playlist_uri = os.environ.get("RUN_PLAYLIST")
    party_playlist_uri = os.environ.get("PARTY_PLAYLIST")
    username = os.environ.get("SPOTIFY_USERNAME")  # My Spotify "username"
    db_username = os.environ.get("PSQL_USERNAME")
    db_password = os.environ.get("PSQL_PASSWORD")
    redirecturi = os.environ.get("REDIRECT_URI") # Spotify requires you to create a redirect_uri.  For now, it's localhost

# Configures the app when it's ran locally and variables are pulled from .env
elif os.getenv("IS_DEV"):
    print("LOCAL DEV")
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOITPY_CLIENT_SECRET")
    discover_playlist_uri = os.getenv("DISCOVER_WEEKLY_PLAYLIST")
    starred_playlist_uri = os.getenv("STARRED_PLAYLIST")
    run_playlist_uri = os.getenv("RUN_PLAYLIST")
    party_playlist_uri = os.getenv("PARTY_PLAYLIST")
    username = os.getenv("SPOTIFY_USERNAME")  # My Spotify "username"
    db_username = os.getenv("PSQL_USERNAME")
    db_password = os.getenv("PSQL_PASSWORD")
    redirecturi = 'http://127.0.0.1:9090' # Spotify requires you to create a redirect_uri.  For now, it's localhost

else:
    print("FALSE")

# Connecting to the existing CRC_DB database
db = psycopg2.connect(
    database="CRC_DB",
    user=db_username,
    password=db_password,
    host="localhost",
    port="5432")

# Scope required to access my private playlist Discover Weekly
playlist_scope = "playlist-read-private"
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret))
playlist_results = sp.user_playlist_tracks(
    user=username, playlist_id=discover_playlist_uri, fields='items, name')
tracks = playlist_results['items']



######## Functions #########

def insert_tracks(artist, title, album, URI, URL):
    cursor = db.cursor()
    sql_to_execute = """INSERT INTO spotify_tracks ("Artist", "Title", "Album", "URI", "URL") VALUES (%s, %s, %s, %s, %s)"""
    sql_values = (artist, title, album, URI, URL)
    cursor.execute(sql_to_execute, sql_values)
    db.commit()

def retrieve_track_info():
    cursor = db.cursor()
    sql_to_execute = """SELECT * FROM spotify_tracks"""
    cursor.execute(sql_to_execute)
    retrieved_tracks = cursor.fetchall()
    return retrieved_tracks
    # for track in retrieved_tracks:
    #     print(f"{track[1]} by {track[0]} from {track[2]} || {track[3]} || {track[4]}")

def weekly_scheduler():
    current_time = datetime.now().strftime("%A %H:%M")  # Returns current Day of the Week and Hour:Minute  

    if current_time == "Monday 12:00":
        for i in range(len(tracks)):
            # (artist, title, album, URI, URL)
            insert_tracks(tracks[i]['track']['artists'][0]['name'],             # Artist name
                            tracks[i]['track']['name'],                         # Song/track name
                            tracks[i]['track']['album']['name'],                # Album name
                            tracks[i]['track']['uri'],                          # Song/track URI  (unique spotify-based ID)
                            tracks[i]['track']['external_urls']['spotify'])     # Spotify song/track URL
    else:
        print(current_time)






















# -------------------------------------------------------------------------------

# class SpotifyAuth:

#     def __init__(self):
#         self.playlist = []
#         self.user = ""

#     def get_response(self):
#         if self.auth_response.status_code == 200:
#             print(self.auth_response)
#         else:
#             print(self.auth_response.status_code)
