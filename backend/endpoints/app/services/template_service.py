import os
import os.path as path
import shutil
import urllib.parse as parse
from flask import current_app as app
from git import Repo, FetchInfo
import logging as log
import tempfile
from dao import user_dao
from uuid import UUID

# u+rw,g+r
ACCESS_RIGHTS = 0o700

username = "CptPicard" # Hardcoded for development
TEMPLATE_REPO_URL = "https://github.com/EficodeEntDemo/PythonTemplateTesting"


def run_template_service(user_uuid: UUID, repo_url: str, template, branch: str = 'main'):
    template_manager = TemplateManager(user_uuid)
    template_manager.push_repo_template(repo_url, template, branch)
    return {'success': True, 'errors': []}


def get_repo_name(url):
    return url.split('/')[-1]


def get_repo_dir(workdir, url):
    return path.join(workdir, get_repo_name(url))


def get_repository(repo_dir, repo_url, checkout=True, branch='main'):
    if not path.isdir(repo_dir):
        repo = Repo.init(repo_dir, bare=False)
        origin = repo.create_remote('origin', repo_url)
        origin.fetch()  # assure we actually have data. fetch() returns useful information

        if checkout:
            if branch == 'main':
                repo.create_head(branch, origin.refs[branch])  # create local branch "master" from remote "master"
                repo.heads.main.set_tracking_branch(origin.refs[branch])  # set local "master" to track remote "master
                repo.heads[branch].checkout()  # checkout local "master" to working tree
            elif branch == 'master':
                repo.create_head(branch, origin.refs[branch])  # create local branch "master" from remote "master"
                repo.heads.master.set_tracking_branch(origin.refs[branch])  # set local "master" to track remote "master
                repo.heads[branch].checkout()  # checkout local "master" to working tree
            else:
                return {'success': False, 'errors': ["Unsupported branch selected! Choose main or master branch."]}
        return repo
    else:
        return Repo(repo_dir)


def pull(repo):
    result = []
    fetch = repo.remotes.origin.pull()
    for info in fetch:
        if info.flags != FetchInfo.HEAD_UPTODATE:
            result.append(info)
    return result


def get_branch_name(info):
    branch = info.name
    return branch[branch.index('/') + len('/'):]


def get_template_name(file_name):
    parts = file_name.split('_')[:-1]
    return ' '.join(parts)


class TemplateManager:

    def __init__(self, user_uuid):
        user_link = user_dao.get_user_link_for_by_user_uuid(user_uuid)
        self.username = username
        self.access_token = user_link.project_user.personal_access_token
        self.repository_url = TEMPLATE_REPO_URL

    def get_repository_url(self, url):
        parts = url.split('://')
        url = parts[0] + '://' + \
              parse.quote(self.username) + ':' + parse.quote(self.access_token) + '@' + parts[1]
        return url

    def refresh_templates(self, workdir):
        repo_dir = get_repo_dir(workdir, self.repository_url)
        repo_url = self.get_repository_url(self.repository_url)
        repo = get_repository(repo_dir, repo_url)
        pull(repo)
        return repo_dir

    def get_template_content(self, template_path):
        self.refresh_templates()
        with open(template_path, 'r') as file:
            return file.read()

    def process_template_file(self, template_path, values_to_replace=None):
        result = self.get_template_content(template_path)
        if values_to_replace:
            for k in values_to_replace.keys():
                result = result.replace(k, values_to_replace[k])
        return result

    def recursive_copy(self, src, dst):
        if not os.path.exists(dst):
            os.makedirs(dst)

        for item in os.listdir(src):
            src_path = path.join(src, item)
            if os.path.isfile(src_path):
                shutil.copy(src_path, dst)

            elif os.path.isdir(src_path):
                new_dst = os.path.join(dst, item)
                os.mkdir(new_dst)
                self.recursive_copy(os.path.abspath(src_path), new_dst)

    def copy_template_dir(self, workdir, template_dir_name, target_dir):
        repo_dir = self.refresh_templates(workdir)
        template_dir = path.join(repo_dir + "/" + template_dir_name)
        self.recursive_copy(template_dir, target_dir)

    def push_repo_template(self, repo_url, template, branch):
        repo_url = self.get_repository_url(repo_url)
        with tempfile.TemporaryDirectory() as workdir:
            repo_dir = get_repo_dir(workdir, repo_url)
            repo = get_repository(repo_dir, repo_url, checkout=False)
            self.copy_template_dir(workdir, template, repo_dir)
            repo.git.checkout('-b', branch)
            repo.git.add('--all')
            repo.git.commit(m='initial commit of Pluto Template files')
            repo.git.push('--set-upstream', 'origin', branch)
