import logging as log
import json
import requests
from flask import current_app as app
from uuid import UUID

from api import db, FUNCTION_NAME_PREFIX
from utils.common import build_result, build_error_result, success_result
from utils.db_common import query_db
from services.github_service import github_auth_headers, update_branch_protection

from ariadne import convert_kwargs_to_snake_case

import boto3

import dao.repository_dao as repository_dao
import dao.project_dao as project_dao
import dao.user_dao as user_dao


class RepositoryExistsException(Exception):
    pass


class RepositoryException(Exception):
    pass


@convert_kwargs_to_snake_case
def get_repository(*_, repository_uuid: UUID):
    return query_db('repository', repository_dao.find_repository, repository_uuid=repository_uuid)


@convert_kwargs_to_snake_case
def add_repository_to_github(obj, info, name: str, description: str, project_uuid: UUID,
                             github_auth_token: str, templates: []):
    try:
        if len(templates) <= 0:
            return build_error_result("No Template given", 400)

        pluto_user = info.context['pluto_user']
        pluto_user_uuid = pluto_user.uuid
        project = project_dao.get_project(pluto_user_uuid, project_uuid)
        user_link = user_dao.get_user_link_by_user_and_project_uuids(info.context['pluto_user'].uuid, project.uuid)

        if repository_dao.repository_exists(project, name):
            raise RepositoryExistsException(f"Repository {name} already exists for project {project.name} in Pluto")

        if user_link.organisation:
            resp = requests.post(f"{app.config['GITHUB_BASE_URL']}orgs/{user_link.organisation.name}/repos",
                                 headers=github_auth_headers(github_auth_token),
                                 json={'name': name, 'body': description})
        else:
            resp = requests.post(f"{app.config['GITHUB_BASE_URL']}user/repos",
                                 headers=github_auth_headers(github_auth_token),
                                 json={'name': name, 'body': description})
        if resp.status_code == 422:
            # 422 gets returned at least for already existing repo
            raise RepositoryExistsException("Repository already exists in GitHub")
        elif resp.status_code != 201:
            log.error(f"Failed to create repository with response code {resp.status_code}: {resp.text}")
            raise RepositoryException("Github repository creation failed")

        repo = repository_dao.insert_repository(resp.json()['html_url'], name, description)
        project.repositories.append(repo)

        if user_link.organisation:
            resp = requests.post(f"{app.config['GITHUB_BASE_URL']}repos/{user_link.organisation.name}/"
                                 f"{repo.name}/projects",
                                 headers=github_auth_headers(github_auth_token),
                                 json={'name': project.name,
                                       'body': project.description})
        else:
            resp = requests.post(f"{app.config['GITHUB_BASE_URL']}repos/{pluto_user.username}/"
                                 f"{repo.name}/projects",
                                 headers=github_auth_headers(github_auth_token),
                                 json={'name': project.name,
                                       'body': project.description})

        if resp.status_code != 201:
            raise Exception(f"Failed to create repository project with response code {resp.status_code}: {resp.text}")

        remote_response = push_repository_template(repo.url, templates, pluto_user_uuid, user_link.uuid, github_auth_token)

        if remote_response.get('success', False) is False:
            log.error(f"Git Lambda failed: {remote_response}")
            raise RepositoryException("Pushing repository template failed")

        update_branch_protection(user_link.organisation.name, repo.name, "main", github_auth_token)

        db.session.commit()

        return build_result("repository", repo.url)
    except RepositoryExistsException as e:
        db.session.rollback()
        return build_error_result("Bad Request", 400, e)
    except RepositoryException as e:
        db.session.rollback()
        return build_error_result("Repository creation failed", 500, e)
    except Exception as e:
        db.session.rollback()
        return build_error_result("Bad request", 400, e)


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
            repo_url = repo.url
            repository_dao.delete_repository(repo.uuid)
            db.session.commit()
            log.warning(f'Repository {repo_url} was not found on GitHub but was deleted from db')
            return success_result()
        elif resp.status_code == 403:
            raise Exception("Repository deletion not allowed on GitHub")
        else:
            raise Exception(f"Failed to delete repository with response code {resp.status_code}: {resp.text}")

    except Exception as e:
        db.session.rollback()
        return build_error_result("Repository deletion failed", 500, e)


def push_repository_template(repo_url: str, template: str, user_uuid: UUID, user_link_uuid: UUID,
                             github_auth_token: str, branch: str = 'main'):
    payload = {'user_uuid': user_uuid,
               'user_link_uuid': str(user_link_uuid),
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
            return json_response
        else:
            raise Exception("Call to git lambda failed")
