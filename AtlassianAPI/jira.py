import os
from shutil import copyfile

import requests
import json


class Jira:

    def __init__(self, base_http_url, project_key, auth):
        self.base_http_url = base_http_url
        self.project_key = project_key
        self.auth = auth

    def create_issue(self, summary, description='', issue_type='Task'):
        # create BitBucket repo
        url = self.base_http_url + 'rest/api/2/issue'
        headers = {'Content-Type': 'application/json'}
        data = {
            "fields": {
                "project": {
                    "key": self.project_key
                },
                "summary": summary,
                "description": description,
                "issuetype": {
                    "name": issue_type
                }
            }
        }

        r = requests.post(url, auth=self.auth, headers=headers, data=json.dumps(data))
        print(json.dumps(data))
        print(r.status_code)
        print(r.text)
        return r

    def get_issues(self, issue_key=None, limit=None):
        if issue_key is None:
            if limit is None:
                url = self.base_http_url + 'rest/api/2/issue?limit=10'
            else:
                url = self.base_http_url + 'rest/api/2/issue?limit=' + str(limit)
        else:
            url = self.base_http_url + 'rest/api/2/issue/' + str(issue_key)
        headers = {'Content-Type': 'application/json'}

        r = requests.get(url, auth=self.auth, headers=headers)
        print(r.status_code)
        print(r.text)
        return r

    def add_attachment(self):
        # TODO: this
        pass
