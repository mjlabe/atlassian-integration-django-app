# ===============
# get user
# ===============
import os
from shutil import copyfile

import requests
import json
from AtlassianIntegration.settings import ATLASSIAN_SETTINGS, STATIC_ROOT
from AtlassianAPI.git.git_commands import *


# [BITBUCKET-BASE-URL], i.e.: https://bitbucket.org/


def create_repo(working_directory, project_key, repo_name):
    # create local git repo
    repo = Git(working_directory)
    repo.git_init()
    copyfile(os.path.join(STATIC_ROOT, 'git', '.gitignore'), os.path.join(working_directory, '.gitignore'))
    repo.git_add_all()
    repo.git_commit_all("init commit")

    # create BitBucket repo
    url = ATLASSIAN_SETTINGS['bitbucket']['http_url'] + 'rest/api/1.0/projects/' + project_key + '/repos'
    headers = {'Content-Type': 'application/json'}
    data = {
        "name": repo_name,
        "scmId": "git",
        "forkable": False,
        "is_private": True
    }

    # get user
    # [USERNAME], i.e.: myuser
    # [PASSWORD], i.e.: itspassword
    username, password = ATLASSIAN_SETTINGS['bitbucket']['username'], ATLASSIAN_SETTINGS['bitbucket']['password']
    r = requests.post(url,
                      auth=(username, password),
                      headers=headers, data=json.dumps(data))
    print(r.status_code)
    print(r.text)
    # print(r.content)

    # ssh: // git @ localhost: 7999 / test / image002jpgcah9adi0mcsea4dgjji2.git
    remote_url = ATLASSIAN_SETTINGS['bitbucket']['ssh_url'] + project_key + '/' + repo_name + '.git'

    # push local repo to BitBucket
    add = repo.git_add_remote(remote_url)
    print(add)
    push = repo.git_push_remote()
    print(push)


def branch_repo(project_key, repo_slug, branch_name):
    # create BitBucket repo
    url = ATLASSIAN_SETTINGS['bitbucket'][
              'http_url'] + 'rest/api/1.0/projects/' + project_key + '/repos/' + repo_slug + '/branches'
    headers = {'Content-Type': 'application/json'}
    data = {
        "name": branch_name,
        "startPoint": "master",
        "message": "created dev branch"
    }

    # get user
    # [USERNAME], i.e.: myuser
    # [PASSWORD], i.e.: itspassword
    r = requests.post(url, auth=(ATLASSIAN_SETTINGS['bitbucket']['username'],
                                 ATLASSIAN_SETTINGS['bitbucket']['password']),
                      headers=headers,
                      data=json.dumps(data))
    print(r.status_code)
    print(r.text)
