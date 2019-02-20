import os
import random
import string
import json
from shutil import copyfile

from django.utils.text import slugify

from AtlassianAPI.git import Git
from AtlassianIntegration.settings import MEDIA_ROOT, STATIC_ROOT, ATLASSIAN_SETTINGS

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.utils.datetime_safe import datetime

from AtlassianAPI.jira import Jira
from AtlassianAPI.bitbucket import BitBucket


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfiles']:
        myfiles = request.FILES.getlist('myfiles')
        upload_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
        uploaded_file_path = os.path.join(MEDIA_ROOT, datetime.now().strftime('%Y%m%d'), upload_id)
        file_name = ""

        if len(myfiles) > 1:
            for file in myfiles:
                fs = FileSystemStorage(location=uploaded_file_path)
                fs.save(file.name, file)
                file_name = file.name

        else:
            file = myfiles[0]
            fs = FileSystemStorage(location=uploaded_file_path)
            fs.save(file.name, file)
            file_name = file.name

        # zip_path = run_console_app(upload_id, uploaded_file_path, file_name)
        #
        # # Serve File
        # # file_path = open(os.path.join(uploaded_file_path, filename_out))
        # file_path = open(zip_path, 'rb')
        # response = HttpResponse(file_path, content_type='application/force-download')
        # response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(os.path.basename(zip_path)) + '.zip'
        # return response

        # initialize repo and commit files
        project_id = ATLASSIAN_SETTINGS['bitbucket']['projects']['TEST']
        repo_slug = slugify(file_name + upload_id)

        # create local git repo
        # TODO: error handling
        repo = Git(uploaded_file_path)
        r1 = repo.git_init()
        copyfile(os.path.join(STATIC_ROOT, 'git', '.gitignore'), os.path.join(uploaded_file_path, '.gitignore'))
        r2 = repo.git_add_all()
        r3 = repo.git_commit("init commit")

        # create bitBucket repo
        # TODO: error handling
        bb_auth = ATLASSIAN_SETTINGS['bitbucket']['username'], ATLASSIAN_SETTINGS['bitbucket']['password']
        bb_http_url = ATLASSIAN_SETTINGS['bitbucket']['http_url']
        bb = BitBucket(base_http_url=bb_http_url, project_key=project_id, auth=bb_auth)
        bb.create_repo(repo_name=repo_slug)

        # push local repo to BitBucket
        # ssh: // git @ localhost: 7999 / test / repo_name.git
        # TODO: error handling
        remote_url = ATLASSIAN_SETTINGS['bitbucket']['ssh_url'] + project_id + '/' + repo_slug + '.git'
        repo.git_add_remote(remote_url)
        repo.git_push_remote()

        # create JIRA issue and branch
        # TODO: better error handling (do more than print)
        auth = ATLASSIAN_SETTINGS['jira']['username'], ATLASSIAN_SETTINGS['jira']['password']
        jira = Jira(base_http_url=ATLASSIAN_SETTINGS['jira']['http_url'], project_key=project_id, auth=auth)

        try:
            issue_key = json.loads(
                jira.create_issue(summary=repo_slug, description='dev branch', issue_type='Task').text)['key']
            # verify issue was created
            issue = jira.get_issues(issue_key).json()
            if issue['key'] != issue_key:
                print('ERROR: Issue not created successfully.' + str(issue))
            bb.branch_repo(repo_name=repo_slug, branch_name=issue_key + '-' + repo_slug + '-dev')
        except ValueError:
            print('Decoding JSON has failed')

        # verify branches were created
        try:
            branches = bb.get_repo_branches(repo_name=repo_slug).json()
            if branches['size'] < 2:
                print('ERROR: Branches not created successfully.' + str(branches))
        except ValueError:
            print('Decoding JSON has failed')

        attachments = [os.path.join('AtlassianAPI', 'test', 'attachments', 'image001.png'),
                       os.path.join('AtlassianAPI', 'test', 'attachments', 'image002.jpg')]

        jira.add_attachment('TEST-35', attachments)

    return render(request, 'simple_upload.html')
