from flask import Flask, render_template, url_for, redirect, flash, session
# from application.spotify_requests import Playlist
from application import app
from application.models import db, SpotifyTracks
# from scheduler import sched

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
    # db.session.refresh(total_tracks)
    return render_template('index.html', home=True, total_tracks=total_tracks, number_of_tracks=number_of_tracks)


@app.route("/highly_recommended")
def highly_recommended():
    return render_template('recommendations.html', rec_selected=True)


@app.route("/testing", methods=['GET', 'POST'])
def testing():
    # discover_weekly.reset_table()
    # discover_weekly.weekly_scheduler()

    SpotifyTracks.select_all()   
    return redirect(url_for('index')) 
    # return render_template('index.html', testing=True, total_tracks=total_tracks, number_of_tracks=number_of_tracks)

# Recreates tables from models.py
@app.route('/testing/createall', methods=['GET', 'POST', 'DELETE'])
def test_create_all():
    db.create_all()
    return redirect(url_for('index'))

# Deletes all tables from database
@app.route('/testing/drop', methods=['GET', 'POST', 'DELETE'])
def test_drop_metrics():
    db.drop_all()
    return redirect(url_for('index'))

@app.route('/testing/droptrack/<int:track_id>', methods=['POST'])
def track_delete(track_id):
    # track = SpotifyTracks.query.filter_by(id=track_id).first()
    track = SpotifyTracks.query.get_or_404(track_id)
    if track:
        db.session.delete(track)
        db.session.commit()
        flash('Item deleted.')
    return redirect(url_for('index'))

@app.route("/testing/add")
def add_songs():
    SpotifyTracks.insert_new_tracks()
    return redirect(url_for('index'))



##################################################################################################
##### Running the App ###### --------------------------------------------------------------
###################################################################################
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)