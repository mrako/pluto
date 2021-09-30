import requests, json
import pprint

AUTH_TOKEN = "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"
PROJECTS_BASE_URL = "https://api.github.com/orgs/EficodeEntDemo/projects"
REPOSITORIES_BASE_URL = "https://api.github.com/orgs/EficodeEntDemo/repos"


def auth_headers():
    return {'Authorization': 'Bearer '+AUTH_TOKEN}


def add_repository_to_github(name, description):
    resp = requests.post(REPOSITORIES_BASE_URL, headers=auth_headers(), json={'name': name,
                                                                              'description': description,
                                                                              'has_projects': True})
    if resp.status_code != 201:
        raise Exception(f"Failed to create repository with response code {resp.status_code}")


def add_project_to_github(name, description):
    resp = requests.post(PROJECTS_BASE_URL, headers=auth_headers(), json={'name': name, 'body': description})
    if resp.status_code != 201:
        raise Exception(f"Failed to create project with response code {resp.status_code}")


def get_repository_info(owner, repo):
    resp = requests.get(f'https://api.github.com/repos/{owner}/{repo}', headers=auth_headers())
    if resp.status_code != 200:
        raise Exception(f"Failed to get repository info with response code {resp.status_code}")
    return resp


def create_repository_from_template(owner, template_repo, name, description):
    resp = requests.post(f'https://api.github.com/repos/{owner}/{template_repo}/generate', headers=auth_headers(), json={'name': name,
                                                                                                                'owner':owner,
                                                                                                                'description': description,
                                                                                                                'private': True})
    print(resp.json())
    if resp.status_code != 201:
        raise Exception(f"Failed to create repository with template: {template_repo} response code {resp.status_code}")