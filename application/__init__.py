from flask import Flask
from dotenv import load_dotenv
from os import getenv, environ
from sqlalchemy import create_engine

app = Flask(__name__)

# Used to configure the app when it's deployed to Heroku
load_dotenv()
if environ.get("IS_HEROKU"):
    # SECRET_KEY = environ.get('SECRET_KEY')
    DATABASE_URI = environ.get('DATABASE_URI')
elif getenv("IS_DEV"):
    SECRET_KEY = getenv('SECRET_KEY')
    DATABASE_URI = getenv('DEV_DATABASE_URI')

app.config.update(
    SECRET_KEY=SECRET_KEY,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_DATABASE_URI=DATABASE_URI
)


DB_URI = app.config['SQLALCHEMY_DATABASE_URI']
engine = create_engine(DB_URI)


# Necessary vvvv
from application import app