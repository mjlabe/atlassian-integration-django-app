import subprocess


def git_init(path, working_directory):
    return subprocess.check_output(['git', 'init', path], cwd=working_directory)


def git_add(file_path, working_directory):
    return subprocess.check_output(['git', 'add', file_path], cwd=working_directory)


def git_add_all(path, working_directory):
    return subprocess.check_output(['git', 'add', '-A', path], cwd=working_directory)


def git_commit(message, working_directory):
    return subprocess.check_output(['git', 'commit',  '-m', message], cwd=working_directory)


def git_commit_all(message, working_directory):
    return subprocess.check_output(['git', 'commit', '-am', message], cwd=working_directory)
