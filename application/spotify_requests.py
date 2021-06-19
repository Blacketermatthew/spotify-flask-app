import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import json
import pandas as pd
import psycopg2
import spotipy  # module for interacting with Spotify
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy.util as util



########## SCOPES ###########
# You have to specify what you'd like to access through pre-defined scopes.
# LIST OF AVAILABLE SCOPES: https://developer.spotify.com/documentation/general/guides/scopes/#user-read-playback-state
# user-top-read: Read access to a user's top artists and tracks.
# playlist-modify-private: Write access to your private playlists
# playlist-modify-public: Same, but for public playlists.


######### VARIABLES #########
load_dotenv()
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOITPY_CLIENT_SECRET")

discover_playlist_uri = os.getenv("DISCOVER_WEEKLY_PLAYLIST")
starred_playlist_uri = os.getenv("STARRED_PLAYLIST")
run_playlist_uri = os.getenv("RUN_PLAYLIST")
party_playlist_uri = os.getenv("PARTY_PLAYLIST")

username = "1242575449"  # My Spotify "username"
redirecturi='http://127.0.0.1:9090'  # Spotify requires you to create a redirect_uri.  For now, it's localhost


# Scope required to access my private playlist Discover Weekly
scope = "playlist-read-private"
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))


results = sp.user_playlist_tracks(user=username, playlist_id=discover_playlist_uri, fields='items, name')
tracks = results['items']


load_dotenv()
db_username = os.getenv("PSQL_USERNAME")
db_password = os.getenv("PSQL_PASSWORD")

db = psycopg2.connect(
    database = "CRC_DB",
    user = db_username,
    password = db_password,
    host = "localhost",
    port = "5432")


def insert_tracks(database, artist, title, album, URI, URL):
    track_data = (artist, title, album, URI, URL)
    cursor = database.cursor()
    sql_to_execute = """INSERT INTO spotify_tracks ("Artist", "Title", "Album", "URI", "URL") VALUES (%s, %s, %s, %s, %s)"""
    sql_values = (artist, title, album, URI, URL)
    cursor.execute(sql_to_execute, sql_values)
    db.commit()

    

for i in range(len(tracks)):
    # print(tracks[i]['track']['artists'][0]['name'], '-',    # Artist name
    # tracks[i]['track']['name'], '| Album:',                 # Song/track name
    # tracks[i]['track']['album']['name'], ' |  URI:',        # Album name         
    # tracks[i]['track']['uri'], '||',                        # Song/track URI  (unique spotify-based ID)
    # tracks[i]['track']['external_urls']['spotify'], '\n'    # Spotify song/track URL
    # )

    # (artist, title, album, URI, URL)
    insert_tracks(db, tracks[i]['track']['artists'][0]['name'], 
        tracks[i]['track']['name'], 
        tracks[i]['track']['album']['name'], 
        tracks[i]['track']['uri'], 
        tracks[i]['track']['external_urls']['spotify'])




# -------------------------------------------------------------------------------

# def write_tracks(text_file, tracks):
#     with open(text_file, 'a') as file_out:
#         while True:
#             for item in tracks['items']:
#                 if 'track' in item:
#                     track = item['track']
#                 else:
#                     track = item
#                 try:
#                     track_url = track['external_urls']['spotify']
#                     file_out.write(track_url + '\n')
#                 except KeyError:
#                     print(u'Skipping track {0} by {1} (local only?)'.format(
#                             track['name'], track['artists'][0]['name']))
#             # 1 page = 50 results
#             # check if there are more pages
#             if tracks['next']:
#                 tracks = spotify.next(tracks)
#             else:
#                 break




### This method prompts the user to confirm access
# token = util.prompt_for_user_token(username, scope=scope, 
#         client_id=client_id, client_secret=client_secret,
#         redirect_uri=redirecturi)

# if token: 
#     sp = spotipy.Spotify(auth=token)
#     playlists = sp.current_user_playlists()

#     while playlists:
#         for i, playlist in enumerate(playlists['items']):
#             print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
#         if playlists['next']:
#             playlists = sp.next(playlists)
#         else:
#             playlists = None
# else:
#     print("Can't get token for", username)







# class SpotifyAuth:

#     def __init__(self):
#         self.playlist = []
#         self.user = ""

#     def get_response(self):
#         if self.auth_response.status_code == 200:
#             print(self.auth_response)
#         else:
#             print(self.auth_response.status_code)




