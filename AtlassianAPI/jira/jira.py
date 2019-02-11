import os
from shutil import copyfile

import requests
import json
from AtlassianIntegration.settings import ATLASSIAN_SETTINGS, STATIC_ROOT


def create_issue(project_key, summary, description='', issue_type='Task'):
    # create BitBucket repo
    url = ATLASSIAN_SETTINGS['jira']['http_url'] + 'rest/api/2/issue'
    headers = {'Content-Type': 'application/json'}
    data = {
        "fields": {
            "project": {
                "key": project_key
            },
            "summary": summary,
            "description": description,
            "issuetype": {
                "name": issue_type
            }
        }
    }

    # get user
    # [USERNAME], i.e.: myuser
    # [PASSWORD], i.e.: itspassword
    r = requests.post(url, auth=(ATLASSIAN_SETTINGS['bitbucket']['username'],
                                 ATLASSIAN_SETTINGS['bitbucket']['password']),
                      headers=headers,
                      data=json.dumps(data))
    print(json.dumps(data))
    print(r.status_code)
    print(r.text)
    return r
