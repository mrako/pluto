import os
import sys
import logging as log

from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL',
                                                       'postgresql://postgres:postgres@localhost:5432/postgres')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

app.config["GITHUB_BASE_URL"] = "https://api.github.com/"
app.config["GITHUB_ACCESS_TOKEN"] = os.environ.get("GITHUB_ACCESS_TOKEN")
app.config["GITHUB_ORG_NAME"] = os.environ.get("GITHUB_ORG_NAME")

root = log.getLogger()
root.setLevel(log.DEBUG)
handler = log.StreamHandler(sys.stdout)
handler.setLevel(log.DEBUG)
formatter = log.Formatter('%(asctime)s %(levelname)s (%(filename)s:%(lineno)d) - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


@app.route('/')
def status():
    return 'UP'
