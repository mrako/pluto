import logging as log
import requests
from flask import current_app as app

# Eventually move all github code here.


class GithubError(Exception):
    pass


def github_auth_headers(token):
    return {'Authorization': 'Bearer '+token}


def update_branch_protection(owner: str, repo_name: str, branch: str, github_auth_token: str):

    payload = {
        'required_status_checks': {
            'strict': True,
            'contexts': []  # What to put here?
        },
        'enforce_admins': True,
        'required_pull_request_reviews': {
            'dismissal_restrictions': {
                'users': [],
                'teams': []
            },
            'dismiss_stale_reviews': True,
            'require_code_owner_reviews': True,
            'required_approving_review_count': 1
        },
        'restrictions': None,
        'required_conversation_resolution': True
    }

    resp = requests.put(f"{app.config['GITHUB_BASE_URL']}repos/{owner}/"
                        f"{repo_name}/branches/{branch}/protection",
                        headers=github_auth_headers(github_auth_token),
                        json=payload)

    if resp.status_code == 403:
        raise GithubError("Github returned Forbidden when updating branch protection")
    elif resp.status_code != 200:
        log.warning(f"Github call failed: {resp.status_code}: {resp.text}")
        raise GithubError("Github call failure, see logs")
