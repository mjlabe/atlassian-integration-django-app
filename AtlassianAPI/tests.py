from django.test import TestCase
import shutil
from AtlassianAPI.bitbucket import *
from AtlassianAPI.jira import *


class AtlassianGitTests(TestCase):

    cwd = os.getcwd()
    test_dir = os.path.join(cwd, 'AtlassianAPI', 'test', 'git_test')

    def git_test(self):

        # create test file
        os.mkdir(self.test_dir)
        f = open(os.path.join(self.test_dir, "git_test.txt"), "w+")
        for i in range(10):
            f.write("This is line %d\r\n" % (i + 1))

        # create git repo
        repo = Git(self.test_dir)
        r = repo.git_init()
        self.assertIs(r.decode('utf-8').startswith('Initialized empty Git repository'), True)
        copyfile(os.path.join(self.cwd, 'AtlassianAPI', 'test', 'git', '.gitignore'), os.path.join(self.test_dir, '.gitignore'))
        repo.git_add_all()
        r = repo.git_status()
        self.assertIs(r.decode('utf-8').startswith(
            'On branch master\n\nNo commits yet\n\nChanges to be committed:\n  '
            '(use "git rm --cached <file>..." to unstage)\n\n\tnew file:   .gitignore\n\tnew file:   git_test.txt'),
                      True)
        r = repo.git_commit_all("init commit")
        self.assertIs(r.decode('utf-8').startswith('[master (root-commit)'), True)

        shutil.rmtree(self.test_dir)

    # TODO: create tests
    def bitbucket_test(self):
        pass

    # TODO: create tests
    def jira_test(self):
        pass

    def cleanup(self):
        shutil.rmtree(self.test_dir)

