from dotenv import load_dotenv
import os
from flask import Flask
import psycopg2


app = Flask(__name__)



if __name__ == "__main__":
    app.run(debug=True, port=5000)
