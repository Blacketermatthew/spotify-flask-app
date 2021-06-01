from flask import Flask, render_template, url_for
from application import app

port = 5000



## Routes ## --------------------------------------
@app.route("/")
@app.route("/index")
@app.route('/home')
def index():
    return render_template('index.html', home=True)

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
    