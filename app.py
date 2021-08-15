from flask import Flask, render_template, url_for
from application.spotify_requests import Playlist, create_database
import psycopg2
from application import app, db
from scheduler import sched

discover_weekly = Playlist("Discover Weekly")

## Routes ## --------------------------------------
@app.route("/")
@app.route("/index")
@app.route('/home')
def index():

    # discover_weekly.weekly_scheduler()
    total_tracks = discover_weekly.retrieve_track_info()

    number_of_tracks = len(total_tracks)
    # for track in total_tracks:
    #     print(track[0])

    return render_template('index.html', home=True, total_tracks=total_tracks, number_of_tracks=number_of_tracks)

@app.route("/highly_recommended")
def highly_recommended():
    return render_template('recommendations.html', rec_selected=True)

@app.route("/two")
def two():
    return render_template('index.html', two=True)

@app.route("/three")
def three():
    return render_template('index.html', three=True)



## App run ## -------------------------------------
if __name__ == "__main__":
    # sched.start()
    create_database()
    db.create_all()
    app.run(debug=True)