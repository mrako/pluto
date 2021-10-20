import os
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))) + "/app")
sys.path.insert(0, dirname(dirname(abspath(__file__))) + "/migrations")
sys.path.insert(0, dirname(dirname(abspath(__file__))))

import logging as log

from flask import Flask
from flask_alembic import Alembic
from flask_sqlalchemy import SQLAlchemy

from utils.response_utils import build_response


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
        alembic = Alembic()
        alembic.init_app(app, run_mkdir=False)
        app.config['ALEMBIC']['script_location'] = 'versions'

        with app.app_context():
            alembic.upgrade()
            return build_response({'success': True, 'message': 'Database migrated successfully'}, 200)
    except Exception:
        message = "Running database migration failed"
        log.exception(message)
        return build_response({'success': False, 'message': message}, 500)
