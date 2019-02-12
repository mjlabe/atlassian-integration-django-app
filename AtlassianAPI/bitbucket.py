import requests
import json


class BitBucket:

    def __init__(self, base_http_url, project_key, auth):
        self.base_http_url = base_http_url
        self.project_key = project_key
        self.auth = auth

    def create_repo(self, repo_name):

        # create BitBucket repo
        url = self.base_http_url + 'rest/api/1.0/projects/' + self.project_key + '/repos'
        headers = {'Content-Type': 'application/json'}
        data = {
            "name": repo_name,
            "scmId": "git",
            "forkable": False,
            "is_private": True
        }

        # POST request
        return requests.post(url, auth=self.auth, headers=headers, data=json.dumps(data))

    def branch_repo(self, repo_name, branch_name):
        # create BitBucket repo
        url = self.base_http_url + 'rest/api/1.0/projects/' + self.project_key + '/repos/' + repo_name + '/branches'
        headers = {'Content-Type': 'application/json'}
        data = {
            "name": branch_name,
            "startPoint": "master",
            "message": "created dev branch"
        }

        # POST request
        return requests.post(url, auth=self.auth, headers=headers, data=json.dumps(data))

    def get_repo_branches(self, repo_name):
        # create BitBucket repo
        url = self.base_http_url + 'rest/api/1.0/projects/' + self.project_key + '/repos/' + repo_name + '/branches'
        headers = {'Content-Type': 'application/json'}

        # GET request
        return requests.get(url, auth=self.auth, headers=headers)

    def get_repos(self, limit):
        # create BitBucket repo
        url = self.base_http_url + 'rest/api/1.0/projects/' + self.project_key + '/repos/?limit=' + str(limit)
        headers = {'Content-Type': 'application/json'}

        # GET request
        return requests.get(url, auth=self.auth, headers=headers)
