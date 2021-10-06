import requests
import logging as log
from flask import current_app as app
from uuid import UUID
from util import query_db, add_error, github_auth_headers, fail_with

from ariadne import convert_kwargs_to_snake_case

from repository_dao import find_repository, insert_repository, find_repository_by_url
from project_dao import insert_project


@convert_kwargs_to_snake_case
def get_repository(*_, repository_uuid: UUID):
    return query_db('repository', find_repository, repository_uuid=repository_uuid)


def add_repository_to_github(*_, url: str, name: str, description: str):
    if find_repository_by_url(url):
        return fail_with("Repository with given url already exists")

    # Need to rethink the transactions here, if github calls fail db should roll back
    result = query_db('repository', insert_repository, url=url, name=name, description=description)
    if not result['success']:
        return result
    repo = result['repository']

    resp = requests.post(app.config['GITHUB_BASE_URL']+"orgs/EficodeEntDemo/repos", headers=github_auth_headers(),
                         json={'url': url, 'name': name, 'body': description})
    if resp.status_code != 201:
        log.warning(f"Failed to create repository with response code {resp.status_code}: {resp.text}")
        return fail_with("Github repository creation failed")

    # Add repository project
    proj_name = f"Repo {name} project"
    proj_desc = "Auto-generated project for repository"

    proj_ins_result = query_db('project', insert_project, name=proj_name, description=proj_desc, repository=repo)
    if not proj_ins_result['success']:
        return result

    resp = requests.post(app.config['GITHUB_BASE_URL']+f"repos/EficodeEntDemo/{name}/projects",
                         headers=github_auth_headers(),
                         json={'name': proj_ins_result['project'].name,
                               'body': proj_ins_result['project'].description})

    if resp.status_code != 201:
        log.warning(f"Failed to create repository project with response code {resp.status_code}: {resp.text}")
        return fail_with("Github repository project creation failed")

    return result

