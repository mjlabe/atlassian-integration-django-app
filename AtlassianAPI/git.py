import subprocess


class Git:
    """
    Common git commands from within a specific working directory.

    """

    def __init__(self, working_directory):
        """Set working_directory where the git repository will reside.

        :param working_directory: Path to the working_directory where the git repository will reside.
        :type working_directory: str
        """

        self.working_directory = working_directory

    def git_init(self):
        """This command creates an empty Git repository in the working_directory path.

        :return: stdout of the process or error codes
        :rtype: str
        """

        return subprocess.check_output(['git', 'init', self.working_directory], cwd=self.working_directory)\
            .decode("utf-8")

    def git_add(self, file_path):
        """Add a file to the staging area by using the "git add" command.

        :param file_path:
        :type file_path: str
        :return: stdout of the process or error codes
        :rtype: str
        """

        return subprocess.check_output(['git', 'add', file_path], cwd=self.working_directory).decode("utf-8")

    def git_add_all(self):
        """Add all files to the staging area by using the "git add --all" command.

        :return: stdout of the process or error codes
        :rtype: str
        """

        return subprocess.check_output(['git', 'add', '--all', self.working_directory], cwd=self.working_directory)\
            .decode("utf-8")

    def git_status(self):
        """Get all paths hat have differences since last commit or that are not tracked by Git.

        Displays paths that have differences between the index file and the current HEAD commit, paths that have
        differences between the working tree and the index file, and paths in the working tree that are not tracked by
        Git.

        :return: stdout of the process or error codes
        :rtype: str
        """

        return subprocess.check_output(['git', 'status', self.working_directory], cwd=self.working_directory)\
            .decode("utf-8")

    def git_commit(self, message):
        """Record changes to the repository

        Stores the current contents of the index in a new commit along with a log message from the user describing the
        changes.

        :param message: A log message from the user describing the changes
        :type message: str
        :return: stdout of the process or error codes
        :rtype: str
        """

        return subprocess.check_output(['git', 'commit',  '-m', message], cwd=self.working_directory).decode("utf-8")

    def git_commit_all(self, message):
        """Staging the file and committing it in one step.

        The “git commit -a” command is a shortcut to a two-step process. After you modify a file that is already known
        by the repo, you still have to tell the repo, “Hey! I want to add this to the staged files and eventually commit
        it to you.” That is done by issuing the “git add” command. “git commit -a” is staging the file and committing it
        in one step.

        :param message: A log message from the user describing the changes
        :type message: str
        :return: stdout of the process or error codes
        :rtype: str
        """

        return subprocess.check_output(['git', 'commit', '-am', message], cwd=self.working_directory).decode("utf-8")

    def git_add_remote(self, remote_url, remote_name='origin'):
        """Manage the set of repositories ("remotes") whose branches you track.

        Adds a remote named <remote_name> for the repository at <remote_url>. To add a new remote, use the git remote
        add command on the terminal, in the directory your repository is stored at. The git remote add command takes two
        arguments: A remote name, for example, origin and a remote URL, for example, https://github.com/user/repo.git.

        :param remote_url: URL of the remote repository
        :type remote_url: str
        :param remote_name: Name of the remote repository (i.e. 'origin')
        :type remote_name: str
        :return: stdout of the process or error codes
        :rtype: str
        """

        return subprocess.check_output(['git', 'remote', 'add', remote_name, remote_url], cwd=self.working_directory)\
            .decode("utf-8")

    def git_push_remote(self, remote_name='origin', branch='master'):
        """Update remote refs along with associated objects

        Updates remote refs using local refs, while sending objects necessary to complete the given refs. The "remote"
        repository is the destination of a push operation. This parameter can be either a URL or the name of a remote.
        The <branch> tells which ref on the remote side is updated with this push. For every branch that is up to date
        or successfully pushed, add upstream (tracking) reference.

        :param remote_name: Name of the remote repository (i.e. 'origin')
        :param branch: Name of the remote branch to push to (i.e. 'master')
        :return: stdout of the process or error codes
        :rtype: str
        """

        return subprocess.check_output(['git', 'push', '-u', remote_name, branch], cwd=self.working_directory)\
            .decode("utf-8")
