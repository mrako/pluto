import os
import sys
import logging as log

from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

ENVIRONMENT_NAME = os.environ.get('ENVIRONMENT_NAME', None)
FUNCTION_NAME_PREFIX = f"pluto-{ENVIRONMENT_NAME}-" if ENVIRONMENT_NAME is not None else ''
BASE_ROUTE = os.environ.get('BASE_ROUTE', '/')

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL',
                                                       'postgresql://pluto:pluto@localhost:5432/pluto')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


app.config["GITHUB_BASE_URL"] = "https://api.github.com/"
app.config["GITHUB_ACCESS_TOKEN"] = os.environ.get("GITHUB_ACCESS_TOKEN")
app.config["GITHUB_ORG_NAME"] = os.environ.get("GITHUB_ORG_NAME")
app.config["USERNAME"] = os.environ.get("GITHUB_USERNAME")
app.config["TEMPLATE_REPO_URL"] = "https://github.com/EficodeEntDemo/PythonTemplateTesting"
app.config["GIT_LAMBDA_LOCAL_URL"] = os.environ.get("GIT_LAMBDA_LOCAL_URL")

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
