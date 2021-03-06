import os
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))) + "/app")
sys.path.insert(0, dirname(dirname(abspath(__file__))) + "/migrations")
sys.path.insert(0, dirname(dirname(abspath(__file__))))

import logging as log

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from utils.response_utils import build_response

app = Flask(__name__)

POSTGRESQL_SUPER_USER = os.environ.get('POSTGRESQL_SUPER_USER', 'postgres')
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
    return setup_db(event)


def setup_db(event):
    action = event.get('action', None)
    try:
        if action:
            if action == "create":
                return create_db(event)
            elif action == "drop-db":
                return drop_db(event)
            elif action == "drop-user":
                return drop_user(event)
            else:
                return build_response({
                    'success': False,
                    'message': "Unknown action. Valid actions are 'create', 'drop-db' and 'drop-user'"},
                    400)
        else:
            return build_response({'success': False, 'message': "Action not defined"}, 400)
    except Exception:
        message = f"setup db failed! Action {action}"
        log.exception(message)
        return build_response({'success': False, 'message': message}, 500)


def create_db(event):
    log.info("Creating database role and schema")
    db.session.connection().connection.set_isolation_level(0)
    db_username = event['owner']
    if not postgres_user_exists(db_username):
        add_postgres_user(username=db_username, password=event['password'])
    create_datatabase(db_name=event['db_name'], owner=db_username)
    return build_response({'success': True, 'message': 'Database role and schema created'}, 200)


def drop_db(event):
    log.info("Dropping database schema")
    db.session.connection().connection.set_isolation_level(0)
    db_name = event['db_name']
    if "'" in db_name:
        raise Exception("Bad database name")

    db.session.execute("DROP DATABASE " + db_name)
    db.session.commit()
    return build_response({'success': True, 'message': 'Database schema dropped'}, 200)


def drop_user(event):
    log.info("Dropping database user")
    db.session.connection().connection.set_isolation_level(0)
    username = event['username']
    if "'" in username:
        raise Exception("Bad database name")

    db.session.execute("DROP USER " + username)
    db.session.commit()
    return build_response({'success': True, 'message': 'Database user dropped'}, 200)


def postgres_user_exists(user_name):
    result = db.session.execute('select rolname from pg_catalog.pg_roles where rolname = :user_name',
                                {'user_name': user_name})
    for row in result:
        return True
    return False


def add_postgres_user(username, password):
    if "'" in username:
        raise Exception("Bad username")

    db.session.execute("CREATE ROLE " + username + " LOGIN PASSWORD :password",
                       {'password': password})
    db.session.commit()


def create_datatabase(db_name: str, owner: str):
    if "'" in db_name:
        raise Exception("Bad database name")

    if "'" in owner:
        raise Exception("Bad db owner")

    db.session.execute("GRANT " + owner + " to " + POSTGRESQL_SUPER_USER)
    db.session.commit()

    db.session.execute("CREATE DATABASE " + db_name +
                       " WITH OWNER=" + owner +
                       " TEMPLATE=template0" +
                       " ENCODING=:encoding" +
                       " LC_COLLATE=:collate" +
                       " LC_CTYPE=:ctype",
                       {'encoding': 'UTF8',
                        'collate': 'en_US.UTF8',
                        'ctype': 'en_US.UTF8'
                        })
    db.session.commit()
