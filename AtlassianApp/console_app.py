import os
import random
import shutil
import string
import subprocess
import zipfile

from AtlassianIntegration.settings import STATIC_ROOT, MEDIA_ROOT

from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.utils.datetime_safe import datetime
from django.utils.encoding import smart_str


def run_console_app(uploaded_file_path, file_name):

    # uploaded_file_path = MEDIA_ROOT + directory
    # filepath = MEDIA_ROOT + directory
    filename_out = "result_" + os.path.splitext(upload_id)[0] + ".doc"

    app = os.path.join(STATIC_ROOT, 'ConsoleApplication')
    p = subprocess.Popen([str(app)], stdin=subprocess.PIPE, shell=True)

    f_in = os.path.join(uploaded_file_path, file_name)
    f_out = os.path.join(uploaded_file_path, filename_out)

    # Commands to send
    # TODO: scan entire directory regardless since a single file will be the only one in the dir
    commands = []
    commands.append("1" + "\n")
    commands.append(f_in + "\n")
    commands.append("2" + "\n")
    commands.append(f_out + "\n")
    commands.append("z" + "\n")

    # issue commands...
    for command in commands:
        p.stdin.write(command.encode('utf-8'))

    p.stdin.close()

    # Wait until process is complete
    p.communicate()

    try:
        # delete files older than today
        for f in os.scandir(MEDIA_ROOT):
            folder = os.fsdecode(f)
            current_folder = os.path.join(MEDIA_ROOT, datetime.now().strftime('%Y%m%d'))
            if folder != current_folder:
                shutil.rmtree(f)
    finally:
        pass

    # zip up files
    zip_path = os.path.join(uploaded_file_path, 'report_' + upload_id + '.zip')
    with zipfile.ZipFile(zip_path, 'w') as myzip:
        myzip.write(f_in, file_name)
        myzip.write(f_out, filename_out)

    return zip_path
