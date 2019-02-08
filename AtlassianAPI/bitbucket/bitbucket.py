# ===============
# get user
# ===============
import requests
import json
from AtlassianIntegration.settings import ATLASSIAN_SETTINGS

# [BITBUCKET-BASE-URL], i.e.: https://bitbucket.org/


url = ATLASSIAN_SETTINGS['bitbucket']['url'] + 'rest/api/1.0/projects/TEST/repos'
headers = {'Content-Type': 'application/json'}

# get user
# [USERNAME], i.e.: myuser
# [PASSWORD], i.e.: itspassword
r = requests.get(url, auth=(ATLASSIAN_SETTINGS['bitbucket']['username'], ATLASSIAN_SETTINGS['bitbucket']['password']), headers=headers)
print(r.status_code)
print(r.text)
# print(r.content)
