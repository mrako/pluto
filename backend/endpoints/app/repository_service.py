import requests
import logging as log
from flask import current_app as app
from uuid import UUID
from api import db
from util import query_db, github_auth_headers, build_result, build_error_result

from ariadne import convert_kwargs_to_snake_case

from repository_dao import find_repository, insert_repository, delete_repository, find_repository_by_url
from dao.project_dao import insert_project


@convert_kwargs_to_snake_case
def get_repository(*_, repository_uuid: UUID):
    return query_db('repository', find_repository, repository_uuid=repository_uuid)


@convert_kwargs_to_snake_case
def add_repository_to_github(*_, url: str, name: str, description: str):
    try:
        if find_repository_by_url(url):
            raise Exception("Repository with given url already exists")

        repo = insert_repository(url, name, description, False)
        resp = requests.post(f"{app.config['GITHUB_BASE_URL']}orgs/{app.config['GITHUB_ORG_NAME']}/repos",
                             headers=github_auth_headers(),
                             json={'url': url, 'name': name, 'body': description})
        if resp.status_code != 201:
            log.warning(f"Failed to create repository with response code {resp.status_code}: {resp.text}")
            raise Exception("Github repository creation failed")

        # Add repository project
        proj = insert_project(name=f"Repository {repo.name}-project",
                              description="Auto-generated project for repository",
                              repository=repo,
                              commit_transaction=False)

        resp = requests.post(f"{app.config['GITHUB_BASE_URL']}repos/{app.config['GITHUB_ORG_NAME']}/"
                             f"{repo.name}/projects",
                             headers=github_auth_headers(),
                             json={'name': proj.name,
                                   'body': proj.description})

        if resp.status_code != 201:
            raise Exception(f"Failed to create repository project with response code {resp.status_code}: {resp.text}")
        db.session.commit()
        return build_result("repository", repo)
    except Exception as e:
        db.session.rollback()
        return build_error_result(str(e), e)


@convert_kwargs_to_snake_case
def delete_repository_from_github(*_, repository_uuid: UUID):
    repo = find_repository(repository_uuid)
    if not repo:
        return {
            'success': False,
            'errors': ["Repository not found"]
        }
    try:
        resp = requests.delete(f"{app.config['GITHUB_BASE_URL']}repos/{app.config['GITHUB_ORG_NAME']}/"
                               f"{repo.name}",
                               headers=github_auth_headers())
        if resp.status_code == 204:
            delete_repository(repo.uuid)
            return {'success': True, 'errors': []}
        elif resp.status_code == 404:  # Is this case sane to handle like this?
            delete_repository(repo.uuid)
            return {'success': True, 'errors': ['Repository was not found on GitHub but was deleted from db']}
        elif resp.status_code == 403:
            raise Exception("Repository deletion not allowed on GitHub")
        else:
            raise Exception(f"Failed to delete repository with response code {resp.status_code}: {resp.text}")
    except Exception as e:
        db.session.rollback()
        return build_error_result(str(e), e)
