import requests
import logging as log
from flask import current_app as app
from uuid import UUID
from api import db
from util import query_db, github_auth_headers, build_result, build_error_result

from ariadne import convert_kwargs_to_snake_case

from repository_dao import find_repository, insert_repository, find_repository_by_url
from project_dao import insert_project


@convert_kwargs_to_snake_case
def get_repository(*_, repository_uuid: UUID):
    return query_db('repository', find_repository, repository_uuid=repository_uuid)


def add_repository_to_github(*_, url: str, name: str, description: str):
    try:
        if find_repository_by_url(url):
            raise Exception("Repository with given url already exists")

        repo = insert_repository(url, name, description, False)
        resp = requests.post(app.config['GITHUB_BASE_URL']+"orgs/EficodeEntDemo/repos", headers=github_auth_headers(),
                             json={'url': url, 'name': name, 'body': description})
        if resp.status_code != 201:
            log.warning(f"Failed to create repository with response code {resp.status_code}: {resp.text}")
            raise Exception("Github repository creation failed")

        # Add repository project
        proj = insert_project(name=f"Repository {name}-project", description="Auto-generated project for repository",
                              repository=repo,
                              commit_transaction=False)

        resp = requests.post(app.config['GITHUB_BASE_URL'] + f"repos/EficodeEntDemo/{repo.name}/projects",
                             headers=github_auth_headers(),
                             json={'name': proj.name,
                                   'body': proj.description})

        if resp.status_code != 201:
            raise Exception(f"Failed to create repository project with response code {resp.status_code}: {resp.text}")

        return build_result("repository", repo)
    except Exception as e:
        db.session.rollback()
        return build_error_result(str(e), e)
