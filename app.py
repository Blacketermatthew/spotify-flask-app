from flask import Flask, render_template, url_for
from application.spotify_requests import discover_weekly
import psycopg2
from application import app, db


## Routes ## --------------------------------------
@app.route("/")
@app.route("/index")
@app.route('/home')
def index():

    discover_weekly.weekly_scheduler()
    total_tracks = discover_weekly.retrieve_track_info()

    # for track in total_tracks:
    #     print(track[0])

    return render_template('index.html', home=True, total_tracks=total_tracks)

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
    app.run(debug=True)