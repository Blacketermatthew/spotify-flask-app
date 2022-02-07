from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql.schema import Column
from application import app
import os
from os import getenv, environ
from dotenv import load_dotenv
import spotipy  # module for interacting with Spotify
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy.util as util
from datetime import datetime



db = SQLAlchemy(app)
migrate = Migrate(app, db)


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
if environ.get("IS_HEROKU"):
    print("\nHEROKU")
    client_id = environ.get("SPOTIPY_CLIENT_ID")
    client_secret = environ.get("SPOITPY_CLIENT_SECRET")
    discover_playlist_uri = environ.get("DISCOVER_WEEKLY_PLAYLIST")
    starred_playlist_uri = environ.get("STARRED_PLAYLIST")
    run_playlist_uri = environ.get("RUN_PLAYLIST")
    party_playlist_uri = environ.get("PARTY_PLAYLIST")
    username = environ.get("SPOTIFY_USERNAME")  # My Spotify "username"
    db_username = environ.get("PSQL_USERNAME")
    db_password = environ.get("PSQL_PASSWORD")
    redirecturi = environ.get("REDIRECT_URI") # Spotify requires you to create a redirect_uri.  For now, it's localhost

# Configures the app when it's ran locally and variables are pulled from .env
elif getenv("IS_DEV"):
    # print("\nLOCAL DEV")
    client_id = getenv("SPOTIPY_CLIENT_ID")
    client_secret = getenv("SPOITPY_CLIENT_SECRET")
    discover_playlist_uri = getenv("DISCOVER_WEEKLY_PLAYLIST")
    starred_playlist_uri = getenv("STARRED_PLAYLIST")
    run_playlist_uri = getenv("RUN_PLAYLIST")
    party_playlist_uri = getenv("PARTY_PLAYLIST")
    username = getenv("SPOTIFY_USERNAME")  # My Spotify "username"
    db_username = getenv("PSQL_USERNAME")
    db_password = getenv("PSQL_PASSWORD")
    redirecturi = 'http://127.0.0.1:5000' # Spotify requires you to create a redirect_uri.  For now, it's localhost

else:
    print("FALSE")


# Scope required to access my private playlist Discover Weekly
playlist_scope = "playlist-read-private"
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
playlist_results = sp.user_playlist_tracks(user=username, playlist_id=discover_playlist_uri, fields='items, name')
tracks = playlist_results['items']


class Playlist:
    
    TrackID = db.Column(db.Integer, primary_key=True)
    Artist = db.Column(db.String(500), nullable=False)
    Track = db.Column(db.String(500), nullable=False)
    Album = db.Column(db.String(500), nullable=False)
    SpotifyURI = db.Column(db.String(1000), nullable=False)
    URL = db.Column(db.String(2000), nullable=False)

    def __init__(self, Artist, Track, Album, SpotifyURI, URL):

        # self.TrackID = TrackID
        self.Artist = Artist
        self.Track = Track
        self.Album = Album
        self.SpotifyURI = SpotifyURI
        self.URL = URL

class SpotifyTracks(db.Model):
    __tablename__ = "spotify_tracks"

    # from . import Column

    TrackID = db.Column(db.Integer, primary_key=True)
    Artist = db.Column(db.String(500), nullable=False)
    Track = db.Column(db.String(500), nullable=False)
    Album = db.Column(db.String(500), nullable=False)
    SpotifyURI = db.Column(db.String(1000), nullable=False)
    URL = db.Column(db.String(2000), nullable=False)

    def __init__(self, Artist, Track, Album, SpotifyURI, URL):

        self.Artist = Artist
        self.Track = Track
        self.Album = Album
        self.SpotifyURI = SpotifyURI
        self.URL = URL

    def reset_table():
        db.session.execute("""TRUNCATE TABLE spotify_tracks RESTART IDENTITY;""")
        db.session.commit()

    def insert_new_tracks():

        # loops through each new song in the Discover Weekly playlist
        for cnt, i in enumerate(range(len(tracks))):
            # (artist, title, album, URI, URL)
        
            uri_list = [row.SpotifyURI for row in SpotifyTracks.query.all()]

            if tracks[i]['track']['uri'] in uri_list:
                print(f"Duplicate: {uri_list[cnt]} - {tracks[i]['track']['artists'][0]['name']}")
                pass
            else:
                print(f"{tracks[i]['track']['name']} by {tracks[i]['track']['artists'][0]['name']} can be added")

                db.session.add(SpotifyTracks(Artist=tracks[i]['track']['artists'][0]['name'],             # Artist name
                                Track=tracks[i]['track']['name'],                         # Song/track name
                                Album=tracks[i]['track']['album']['name'],                # Album name
                                SpotifyURI=tracks[i]['track']['uri'],                          # Song/track URI  (unique spotify-based ID)
                                URL=tracks[i]['track']['external_urls']['spotify']))
        db.session.commit()
            
    def insert_a_track(self, Artist, Track, Album, SpotifyURI, URL):
        try:
            db.session.add(SpotifyTracks(
                Artist=Artist, 
                Track=Track,
                Album=Album,
                SpotifyURI=SpotifyURI,
                URL=URL)
            )
            db.session.commit()
            print("db insert success \n")
        except:
            print("db insert error \n")

    def select_all():
        try:
            table_query = SpotifyTracks.query.all()
            
            results = [
                {
                    'Artist': row.Artist,      
                    'Track': row.Track,                
                    'Album': row.Album,        
                    'SpotifyURI': row.SpotifyURI,                          
                    'URL': row.URL
                } for row in table_query ]


            print(results)
            print("db select all success")

            return table_query

        except:
            print("db select all error")

    def delete_item(self, **kwargs):
        try:
            if kwargs:
                table_query = SpotifyTracks.query.filter_by(**kwargs).all()
                for row in table_query:
                    db.session.delete(row)
            else:
                print("What rows would you like to delete? Try again.")

            db.session.commit()
            print("db delete success")

        except:
            print("db delete error")

