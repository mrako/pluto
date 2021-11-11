import logging as log
import json
import requests
from flask import current_app as app
from uuid import UUID
from api import db, FUNCTION_NAME_PREFIX
from utils.common import build_result, build_error_result, success_result
from utils.db_common import query_db
from utils.github_common import github_auth_headers

from ariadne import convert_kwargs_to_snake_case

import boto3

import dao.repository_dao as repository_dao
import dao.project_dao as project_dao
import dao.user_dao as user_dao


@convert_kwargs_to_snake_case
def get_repository(*_, repository_uuid: UUID):
    return query_db('repository', repository_dao.find_repository, repository_uuid=repository_uuid)


@convert_kwargs_to_snake_case
def add_repository_to_github(obj, info, name: str, description: str, project_uuid: UUID,
                             github_auth_token: str, templates: []):
    try:
        if len(templates) <= 0:
            raise Exception("No templates given")
        user_link = user_dao.get_user_link_by_user_and_project_uuids(info.context['pluto_user'].uuid, project_uuid)

        resp = requests.post(f"{app.config['GITHUB_BASE_URL']}orgs/{user_link.organisation.name}/repos",
                             headers=github_auth_headers(github_auth_token),
                             json={'name': name, 'body': description})
        if resp.status_code == 422:
            raise Exception("Repository already exists")  # 422 gets returned at least for already existing repo
        elif resp.status_code != 201:
            log.warning(f"Failed to create repository with response code {resp.status_code}: {resp.text}")
            raise Exception("Github repository creation failed")

        repo = repository_dao.insert_repository(resp.json()['html_url'], name, description)

        # Get the project that was created earlier

        proj = project_dao.get_project(project_uuid)
        proj.repositories.append(repo)

        resp = requests.post(f"{app.config['GITHUB_BASE_URL']}repos/{user_link.organisation.name}/"
                             f"{repo.name}/projects",
                             headers=github_auth_headers(github_auth_token),
                             json={'name': proj.name,
                                   'body': proj.description})

        if resp.status_code != 201:
            raise Exception(f"Failed to create repository project with response code {resp.status_code}: {resp.text}")

        remote_response = push_repository_template(repo.url, templates, user_link.uuid, github_auth_token)
        log.debug(f"Remote response in api side is {remote_response}")
        if remote_response.get('success', False):
            raise Exception("Remote call to push repository lambda failed")

        db.session.commit()
        return build_result("repository", repo)
    except Exception as e:
        db.session.rollback()
        return build_error_result(str(e), e)


@convert_kwargs_to_snake_case
def delete_repository_from_github(*_, info, repository_uuid: UUID, github_auth_token: str):
    try:
        repo = repository_dao.find_repository(repository_uuid)
        if not repo:
            raise Exception("Repository not found")

        user_link = info.context['pluto_user'].user_link

        resp = requests.delete(f"{app.config['GITHUB_BASE_URL']}repos/{user_link.organisation.name}/"
                               f"{repo.name}",
                               headers=github_auth_headers(github_auth_token))
        if resp.status_code == 204:
            repository_dao.delete_repository(repo.uuid)
            db.session.commit()
            return success_result()
        elif resp.status_code == 404:  # Is this case sane to handle like this?
            repository_dao.delete_repository(repo.uuid)
            db.session.commit()
            return success_result('Repository was not found on GitHub but was deleted from db')
        elif resp.status_code == 403:
            raise Exception("Repository deletion not allowed on GitHub")
        else:
            raise Exception(f"Failed to delete repository with response code {resp.status_code}: {resp.text}")

    except Exception as e:
        db.session.rollback()
        return build_error_result(str(e), e)


def push_repository_template(repo_url: str, template: str, user_link_uuid: UUID,
                             github_auth_token: str, branch: str = 'main'):
    payload = {'user_link_uuid': str(user_link_uuid),
               'github_auth_token': github_auth_token,
               'repo_url': repo_url,
               'template': template,
               'branch': branch}
    if app.config['GIT_LAMBDA_LOCAL_URL']:
        resp = requests.post(app.config['GIT_LAMBDA_LOCAL_URL'], json=payload)
        if resp.status_code != 200:
            raise Exception("HTTP call to local git lambda failed")
        else:
            return resp.json()
    else:
        client = boto3.client('lambda')
        resp = client.invoke(FunctionName=f"{FUNCTION_NAME_PREFIX}pluto-git", InvocationType='RequestResponse',
                             Payload=json.dumps(payload))
        if resp.get('StatusCode', None) == 200:
            json_response = json.loads(resp['Payload'].read().decode("utf-8"))
            # This should be '{"success": true}' on success, '{"success": false, errors: []}' on failure
            log.debug(f"Gitlambda returned {json_response}")
            return json_response
        else:
            raise Exception("Call to git lambda failed")
