import os
import os.path as path
import shutil
import urllib.parse as parse
from os.path import isfile
from os import listdir
from flask import current_app as app
from git import Repo, FetchInfo
from models import Template
import logging as log
import template_dao
from ariadne import convert_kwargs_to_snake_case
import stat
import tempfile
from pluto_multiprocess import execute_in_child_process


# u+rw,g+r
ACCESS_RIGHTS = 0o700


@convert_kwargs_to_snake_case
def run_template_service(*_, repo_url: str, template, branch: str = 'main'):
    username = app.config["USERNAME"]
    template_manager = TemplateManager(username)
    execute_in_child_process(template_manager.push_repo_template, repo_url, template, branch)
    return {'success': True, 'errors': []}


@convert_kwargs_to_snake_case
def delete_all_files_from_repository(*_, repo_name: str, repo_url: str, branch: str = 'main'):
    username = app.config["USERNAME"]
    template_manager = TemplateManager(username)
    template_manager.clear_repository(repo_name, repo_url, branch)


def get_repo_name(url):
    return url.split('/')[-1]


def get_repo_dir(workdir, url):
    return path.join(workdir, get_repo_name(url))


def on_rm_error( func, path, exc_info):
    # path contains the path of the file that couldn't be removed
    # let's just assume that it's read-only and unlink it.
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)


def prepare_work_dir(workdir):
    if not path.isdir(workdir):
        log.info("Creating directory {}".format(workdir))
        os.makedirs(workdir, mode=ACCESS_RIGHTS)


def save_file(file_path, content):
    if not path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write(content)
    else:
        raise Exception("ERROR: Path {} already exists!".format(file_path))


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

    #todo
    def __init__(self, username):
        self.username = username
        self.access_token = app.config["GITHUB_ACCESS_TOKEN"]
        self.repository_url = app.config["TEMPLATE_REPO_URL"]
        self.access_token = app.config["GITHUB_ACCESS_TOKEN"]
        self.workdir = app.config["WORKDIR"]

    def get_repository_url(self, url):
        parts = url.split('://')
        url = parts[0] + '://' + \
              parse.quote(self.username) + ':' + parse.quote(self.access_token) + '@' + parts[1]
        return url

    def get_target_name(self, template_name, file_name):
        target_name = template_dao.find_template(template_name)
        if target_name.target_name:
            return target_name

        return file_name

    def refresh_templates(self):
        workdir = self.workdir
        prepare_work_dir(workdir)
        repo_dir = get_repo_dir(workdir, self.repository_url)
        repo_url = self.get_repository_url(self.repository_url)
        repo = get_repository(repo_dir, repo_url)
        pull(repo)
        return repo_dir

    def get_templates(self, template_name):
        repo_dir = self.refresh_templates()
        template_dir = path.join(repo_dir + "/" + template_name)

        templates = []
        for file_name in listdir(template_dir):
            template_path = path.join(template_dir, file_name)
            if isfile(template_path):
                templates.append(Template(
                    name=get_template_name(file_name),
                    path=template_path,
                    target_name=self.get_target_name(template_name, file_name),
                    template=template_name
                ))
                template_dao.insert_template(Template(
                    name=get_template_name(file_name),
                    path=template_path,
                    target_name=self.get_target_name(template_name, file_name),
                    template=template_name
                ))
        return templates

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

    def copy_template_dir(self, template_dir_name, target_dir):
        repo_dir = self.refresh_templates()
        template_dir = path.join(repo_dir + "/" + template_dir_name)
        self.recursive_copy(template_dir, target_dir)

    def push_repo_template(self, repo_url, template, branch):
        repo_url = self.get_repository_url(repo_url)
        with tempfile.TemporaryDirectory() as tmpdirname:
            self.workdir = tmpdirname
            repo_dir = get_repo_dir(tmpdirname, repo_url)
            prepare_work_dir(tmpdirname)
            repo = get_repository(repo_dir, repo_url, checkout=False)
            self.copy_template_dir(template, repo_dir)

            repo.git.checkout('-b', branch)
            repo.git.add('--all')
            repo.git.commit(m='initial commit of Pluto Template files')
            repo.git.push('--set-upstream', 'origin', branch)

    def clear_repository(self, repo_name, repo_url, branch):
        """
        This method deletes all files from a repository
        """
        repo_url = self.get_repository_url(repo_url)
        workdir = path.join(self.workdir, repo_name)
        repo_dir = get_repo_dir(workdir, repo_url)
        repo = get_repository(repo_dir, repo_url, branch=branch)
        pull(repo)
        if not os.path.exists(repo_dir):
            log.warning("cannot clear the repository - directory does not exist")
        else:
            for item in os.listdir(repo_dir):
                src_path = path.join(repo_dir, item)
                if os.path.isfile(src_path):
                    os.remove(src_path)
                    print(f"deleted {item}")

                elif os.path.isdir(src_path) and item != '.git':
                    shutil.rmtree(src_path)
                    print(f"deleted {item}")
        repo.git.add('--all')
        repo.git.commit(m='initial commit of Pluto Template files')
        repo.git.push('--set-upstream', 'origin', branch)
        return {'success': True, 'errors': []}
