from flask import Flask
from dotenv import load_dotenv
import os
import psycopg2


app = Flask(__name__)


load_dotenv()
if os.environ.get("IS_HEROKU"):
    database_url = os.environ.get('DATABASE_URL')
    db_username = os.environ.get("PSQL_USERNAME")
    db_password = os.environ.get("PSQL_PASSWORD")
    # Connect to the postgres database in Heroku
    db = psycopg2.connect(database_url)

elif os.getenv("IS_DEV"):
    db_username = os.getenv("PSQL_USERNAME")
    db_password = os.getenv("PSQL_PASSWORD")

    # Connecting to the existing local CRC_DB database
    try:
        db = psycopg2.connect(
            database="CRC_DB",
            user=db_username,
            password=db_password,
            host="localhost",
            port="5432")
    except:
        print("dev db connect fail")

else:
    print("CONFIG ERROR")



