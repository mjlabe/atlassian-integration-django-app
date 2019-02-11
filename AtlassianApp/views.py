import os
import random
import shutil
import string
import subprocess
import zipfile
from shutil import copyfile
import json

from django.utils.text import slugify

from AtlassianIntegration.settings import STATIC_ROOT, MEDIA_ROOT

from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.utils.datetime_safe import datetime
from django.utils.encoding import smart_str

from AtlassianAPI.bitbucket.bitbucket import create_repo, branch_repo
from AtlassianAPI.jira.jira import create_issue


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
        project_id = 'TEST'
        repo_slug = slugify(file_name + upload_id)
        create_repo(working_directory=uploaded_file_path, project_key=project_id, repo_name=repo_slug)
        issue_key = json.loads(create_issue(project_key=project_id, summary=repo_slug, issue_type='Task').text)['key']
        branch_repo(project_key=project_id, repo_slug=repo_slug, branch_name=issue_key + '-' + repo_slug + '-dev')

        # create bitbucket repo and push

    return render(request, 'simple_upload.html')
