import os
import sys
import logging as log

from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

BASE_ROUTE = os.environ.get('BASE_ROUTE', '/')

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL',
                                                       'postgresql://pluto:pluto@localhost:5432/pluto')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


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
