import requests, json

AUTH_TOKEN = "YOUR_GITHUB_TOKEN_HERE"
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

