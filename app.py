from flask import Flask, render_template, url_for
# from application.spotify_requests import Playlist
from application import app
from application.models import db, SpotifyTracks
from scheduler import sched

discover_weekly = SpotifyTracks
total_tracks = SpotifyTracks.query.all()
number_of_tracks = len(total_tracks)

##################################################################################################
##### Routes ###### -----------------------------------------------------------------------
###################################################################################
@app.route("/")
@app.route("/index")
@app.route('/home')
def index():
    return render_template('index.html', home=True, total_tracks=total_tracks, number_of_tracks=number_of_tracks)


@app.route("/highly_recommended")
def highly_recommended():
    return render_template('recommendations.html', rec_selected=True)


@app.route("/testing", methods=['GET', 'POST'])
def testing():
    # discover_weekly.reset_table()
    # discover_weekly.weekly_scheduler()

    SpotifyTracks.select_all()    
    return render_template('index.html', testing=True, total_tracks=total_tracks, number_of_tracks=number_of_tracks)


@app.route("/add")
def add():
    SpotifyTracks.insert_new_tracks()
    return render_template('index.html', add=True, total_tracks=total_tracks, number_of_tracks=number_of_tracks)


##################################################################################################
##### Running the App ###### --------------------------------------------------------------
###################################################################################
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)