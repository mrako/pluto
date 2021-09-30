import os
import sys
import logging as log
from flask import Flask
from flask_alembic import Alembic
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DATABASE_URL']
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

root = log.getLogger()
root.setLevel(log.DEBUG)
handler = log.StreamHandler(sys.stdout)
handler.setLevel(log.DEBUG)
formatter = log.Formatter('%(asctime)s %(levelname)s (%(filename)s:%(lineno)d) - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


def handler(event, context):
    try:
        log.info("Migrating the database schema")
        log.info(f"Current directory {os.getcwd()}")
        log.info(f"Context {context}")
        alembic = Alembic()
        alembic.init_app(app)
        log.info(f"Script directory {app.config['ALEMBIC']['script_location']}")

        with app.app_context():
            return alembic.upgrade()
    except Exception as e:
        log.exception("Running database migration failed")
        raise e