import os
import sys
import logging as log
import json
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


def build_response(result: dict, status_code: int):
    return {
        'statusCode': f"{status_code}",
        'body': json.dumps(result),
        'headers': {
            'Content-Type': 'application/json',
        }
    }


def handler(event, context):
    try:
        log.info("Migrating the database schema")
        alembic = Alembic()
        alembic.init_app(app, run_mkdir=False)
        app.config['ALEMBIC']['script_location'] = 'versions'

        with app.app_context():
            alembic.upgrade()
            return build_response({'success': True, 'message': 'Database migrated successfully'}, 200)
    except Exception as e:
        message = "Running database migration failed"
        log.exception(message)
        return build_response({'success': False, 'message': message}, 500)
