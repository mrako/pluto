from flask import current_app as app


def github_auth_headers():
    return {'Authorization': 'Bearer '+app.config['GITHUB_ACCESS_TOKEN']}
