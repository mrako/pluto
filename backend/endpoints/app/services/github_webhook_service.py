import hashlib
import logging as log
import hmac
from api import db
import dao.data_origin_dao as origin_dao
import dao.organisation_dao as org_dao
from dao import project_dao, user_link_dao
from models import DataOrigin


def validate_github_request_sha256(github_signature, webhook_secret, message) -> bool:
    if not webhook_secret:
        log.error("Github webhook_secret not defined! - Payload validation failed")
        return False

    github_signature = github_signature.strip()
    if not github_signature:
        log.error("No github signature")
        return False
    key = bytes(webhook_secret, 'UTF-8')
    hexdigest = hmac.new(key, message, hashlib.sha256).hexdigest()
    signature = "sha256=" + hexdigest
    result = github_signature == signature
    if not result:
        log.warning("Could not verify request signature! ({} vs. {})".format(github_signature, signature))
    return result


def find_org(data_origin: DataOrigin, installation_id: int, account: dict, create: bool = False):
    org = org_dao.find_by_ext_id(data_origin, account['id'])
    if org is None and create is True:
        org = org_dao.create_org(data_origin, installation_id, account['id'], account['login'])
        db.session.commit()
    return org


def find_project_user(data_origin: DataOrigin, installation_id: int, sender: dict, create: bool = False):
    user = project_dao.find_user_by_ext_id(data_origin, sender['id'])
    if user is None and create is True:
        user = project_dao.create_project_user(data_origin, installation_id, sender['id'], sender['login'])
        db.session.commit()
    return user


def register_app_installation(payload: dict):
    data_origin = origin_dao.get_data_origin_by_name('GitHub')
    installation_id = payload['installation']['id']
    account = payload['installation']['account']
    if account['type'] == 'Organization':
        find_org(data_origin, installation_id, account, create=True)
    find_project_user(data_origin, installation_id, payload['sender'], create=True)


def deactivate_app_installation(payload):
    raise Exception("Not Implemented!")


def activate_app_installation(payload):
    raise Exception("Not Implemented!")


def remove_app_installation(payload):
    data_origin = origin_dao.get_data_origin_by_name('GitHub')
    installation_id = payload['installation']['id']
    account = payload['installation']['account']
    if account['type'] == 'Organization':
        org = find_org(data_origin, installation_id, account, create=True)
        user_link_dao.delete_organisation_links(org.uuid)
        db.session.delete(org)
    user = find_project_user(data_origin, installation_id, payload['sender'], create=True)
    user_link_dao.delete_user_links(user.uuid)
    db.session.delete(user)
    db.session.commit()
