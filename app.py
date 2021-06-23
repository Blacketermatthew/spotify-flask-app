from flask import Flask, render_template, url_for
from application import app
from application.spotify_requests import retrieve_track_info, insert_tracks

port = 5000



## Routes ## --------------------------------------
@app.route("/")
@app.route("/index")
@app.route('/home')
def index():

    total_tracks = retrieve_track_info()

    # for track in total_tracks:
    #     print(track[0])

    return render_template('index.html', home=True, total_tracks=total_tracks)



@app.route("/one")
def one():
    return render_template('index.html', one=True)

@app.route("/two")
def two():
    return render_template('index.html', two=True)

@app.route("/three")
def three():
    return render_template('index.html', three=True)







## App run ## -------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=port)
    