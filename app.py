from flask import Flask, render_template, url_for
# from application.spotify_requests import Playlist
# import psycopg2
from application import app
from application.models import db, SpotifyTracks
from scheduler import sched

discover_weekly = SpotifyTracks

## Routes ## --------------------------------------
@app.route("/")
@app.route("/index")
@app.route('/home')
def index():

    # discover_weekly.reset_table()
    # discover_weekly.weekly_scheduler()
    total_tracks = SpotifyTracks.query.all()

    number_of_tracks = len(total_tracks)
    # for track in total_tracks:
    #     print(track[0])

    return render_template('index.html', home=True, total_tracks=total_tracks, number_of_tracks=number_of_tracks)


@app.route("/highly_recommended")
def highly_recommended():
    return render_template('recommendations.html', rec_selected=True)


@app.route("/testing", methods=['GET', 'POST'])
def testing():

    # SpotifyTracks.insert_new_tracks()
    
    total_tracks = SpotifyTracks.query.all()

    number_of_tracks = len(total_tracks)
    # SpotifyTracks.select_all()

    return render_template('index.html', testing=True, total_tracks=total_tracks, number_of_tracks=number_of_tracks)


@app.route("/three")
def three():
    return render_template('index.html', three=True)



## App run ## -------------------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # db.session.commit()
    app.run(debug=True)