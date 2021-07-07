import os
from dotenv import load_dotenv
import requests
import json
import psycopg2
import spotipy  # module for interacting with Spotify
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy.util as util
from datetime import datetime
from application import app, db

########## SCOPES ###########
# You have to specify what you'd like to access through pre-defined scopes.
# LIST OF AVAILABLE SCOPES: https://developer.spotify.com/documentation/general/guides/scopes/#user-read-playback-state
# user-top-read: Read access to a user's top artists and tracks.
# playlist-modify-private: Write access to your private playlists
# playlist-modify-public: Same, but for public playlists.


######### VARIABLES #########

## Traditional variables from .env
load_dotenv()


### NOTE: CREATE A CLASS FOR THIS IN A SEPARATE FILE? #############

# Used to configure the app when it's deployed to Heroku
if os.environ.get("IS_HEROKU"):
    print("\nHEROKU")
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
    print("\nLOCAL DEV")
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOITPY_CLIENT_SECRET")
    discover_playlist_uri = os.getenv("DISCOVER_WEEKLY_PLAYLIST")
    starred_playlist_uri = os.getenv("STARRED_PLAYLIST")
    run_playlist_uri = os.getenv("RUN_PLAYLIST")
    party_playlist_uri = os.getenv("PARTY_PLAYLIST")
    username = os.getenv("SPOTIFY_USERNAME")  # My Spotify "username"
    db_username = os.getenv("PSQL_USERNAME")
    db_password = os.getenv("PSQL_PASSWORD")
    redirecturi = 'http://127.0.0.1:5000' # Spotify requires you to create a redirect_uri.  For now, it's localhost

else:
    print("FALSE")


# Scope required to access my private playlist Discover Weekly
playlist_scope = "playlist-read-private"
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret))
playlist_results = sp.user_playlist_tracks(
    user=username, playlist_id=discover_playlist_uri, fields='items, name')
tracks = playlist_results['items']



class playlist:

    def __init__(self, playlist_title, ):
        self.playlist_title = playlist_title
        self.create_table()

    ######## Functions #########

    def create_table(self):
        try:
            command = """
                CREATE TABLE spotify_tracks (
                        track_id SERIAL PRIMARY KEY,
                        artist VARCHAR(200) NOT NULL,
                        track VARCHAR(200) NOT NULL,
                        album VARCHAR(300) NOT NULL,
                        spotify_uri VARCHAR(200) NOT NULL,
                        url VARCHAR(300) NOT NULL
                        )
                """
            cursor = db.cursor()
            cursor.execute(command)
            db.commit()
        except:
            print(f"Table already exists")
            db.rollback()
        finally:
            # closing database connection.
            if db:
                cursor.close()
                print("PostgreSQL connection is closed (create)\n")


    def insert_tracks(self):
        insert_sql = """INSERT INTO spotify_tracks ("artist", "track", "album", "spotify_uri", "url") VALUES (%s, %s, %s, %s, %s)"""
        # sql_values = (artist, title, album, URI, URL)

        try:
            cursor = db.cursor()
            for i in range(len(tracks)):
                # (artist, title, album, URI, URL)
                sql_values = (tracks[i]['track']['artists'][0]['name'],             # Artist name
                                tracks[i]['track']['name'],                         # Song/track name
                                tracks[i]['track']['album']['name'],                # Album name
                                tracks[i]['track']['uri'],                          # Song/track URI  (unique spotify-based ID)
                                tracks[i]['track']['external_urls']['spotify'])     # Spotify song/track URL
                cursor.execute(insert_sql, sql_values)
            db.commit()

        except:
            print("Nothing to insert right now")
            db.rollback()
        finally:
            # closing database connection.
            if db:
                cursor.close()
                print("PostgreSQL connection is closed (insert)\n")


    def retrieve_track_info(self):
        try:
            cursor = db.cursor()
            select_sql = "SELECT * FROM spotify_tracks"
            cursor.execute(select_sql)
            retrieved_tracks = cursor.fetchall()
            return retrieved_tracks
        except (Exception, psycopg2.Error) as error:
            print("Error:", error)
            db.rollback()
        finally:
            # closing database connection.
            if db:
                cursor.close()
                print("PostgreSQL connection is closed (retrieve)\n")
        # for track in retrieved_tracks:
        #     print(f"{track[1]} by {track[0]} from {track[2]} || {track[3]} || {track[4]}")

    def weekly_scheduler(self):
        current_time = datetime.now().strftime("%A %H:%M")  # Returns current Day of the Week and Hour:Minute  

        if current_time == "Monday 12:00":
            print("playlist time!")
            self.insert_tracks()
        else:
            print(f"Current Time: {current_time}.  The playlist updates every Monday at noon.")



discover_weekly = playlist("Discover Weekly")















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
