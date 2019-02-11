import subprocess


class Git:
    """
    Common git commands from within a specific working directory.

    """

    def __init__(self, working_directory):
        self.working_directory = working_directory

    def git_init(self):
        return subprocess.check_output(['git', 'init', self.working_directory], cwd=self.working_directory)

    def git_add(self, file_path):
        return subprocess.check_output(['git', 'add', file_path], cwd=self.working_directory)

    def git_add_all(self):
        return subprocess.check_output(['git', 'add', '-A', self.working_directory], cwd=self.working_directory)

    def git_status(self):
        return subprocess.check_output(['git', 'status', self.working_directory], cwd=self.working_directory)

    def git_commit(self, message):
        return subprocess.check_output(['git', 'commit',  '-m', message], cwd=self.working_directory)

    def git_commit_all(self, message):
        return subprocess.check_output(['git', 'commit', '-am', message], cwd=self.working_directory)

    def git_add_remote(self, remote_url, remote_name='origin'):
        return subprocess.check_output(['git', 'remote', 'add', remote_name, remote_url], cwd=self.working_directory)

    def git_push_remote(self, remote_name='origin', branch='master'):
        return subprocess.check_output(['git', 'push', '-u', remote_name, branch], cwd=self.working_directory)
