import requests
import json


class BitBucket:
    """Common BitBucket API methods.

    Bitbucket's REST APIs provide access to resources (data entities) via URI paths. To use a REST API, your
    application will make an HTTP request and parse the response. The Bitbucket REST API uses JSON as its communication
    format, and the standard HTTP methods like GET, PUT, POST and DELETE. URIs for Bitbucket's REST API resource have
    the following structure:

    http://host:port/context/rest/api-name/api-version/path/to/resource

    For example, the following URI would retrieve a page of the latest commits to the jira repository in the Jira project on https://stash.atlassian.com.

    https://stash.atlassian.com/rest/api/1.0/projects/JIRA/repos/jira/commits
    """

    def __init__(self, base_http_url, project_key, auth):
        """Initialize BitBucket object with base_http_url, project_key, and auth.

        :param base_http_url: URL for BitBucket site - http://host:port/ (i.e. http://localhost:7990/)
        :type base_http_url: str
        :param project_key: The project matching the projectKey supplied in the resource path as shown in URL.
        :type project_key: str
        :param auth: Tuple of username and password for authentication.
        :type auth: tuple[str, str]
        """
        self.base_http_url = base_http_url
        self.project_key = project_key
        self.auth = auth

    def create_repo(self, repo_name):
        """Create a new repository.

        Requires an existing project in which this repository will be created. The only parameters which will be used
        are name and scmId.

        The authenticated user must have PROJECT_ADMIN permission for the context project to call this resource.

        :param repo_name: Name of repository to create (i.e. "My repo").
        :type repo_name: str
        :return:
            201 - application/json (repository)
            400 - application/json (errors)
            401 - application/json (errors)
            409 - application/json (errors)
        :rtype: requests.Response
        """

        # create BitBucket repo
        url = self.base_http_url + 'rest/api/1.0/projects/' + self.project_key + '/repos'
        headers = {'Content-Type': 'application/json'}
        data = {
            "name": repo_name,
            "scmId": "git",
            "forkable": False,
            "is_private": True
        }

        # POST request
        return requests.post(url, auth=self.auth, headers=headers, data=json.dumps(data))

    def get_repos(self, limit=10, start_at=0):
        """Retrieve repositories from the project corresponding to the supplied projectKey.

        This is a paged API. This API can also be invoked via a user-centric URL when addressing repositories in
        personal projects.

        The authenticated user must have REPO_READ permission for the specified project to call this resource.

        :param limit: Number of repos to get.
        :type limit: int
        :param start_at: Item that should be used as the first item in the page of results.
        :type start_at: int
        :return:
            200 - application/json (repository)
            401 - application/json (errors)
            404 - application/json (errors)
        :rtype: requests.Response
        """

        # create BitBucket repo
        url = self.base_http_url + 'rest/api/1.0/projects/' + self.project_key + '/repos/?limit=' + str(limit) + \
                                   '&startAt' + str(start_at)
        headers = {'Content-Type': 'application/json'}

        # GET request
        return requests.get(url, auth=self.auth, headers=headers)

    def branch_repo(self, repo_name, branch_name):
        """Creates a branch using the information provided in the {@link RestCreateBranchRequest request}

        The authenticated user must have REPO_WRITE permission for the context repository to call this resource.

        :param repo_name: Name of repository where branch is created (i.e. "my_repo").
        :type repo_name: str
        :param branch_name: Name of branch to create (i.e. "my_branch").
        :type branch_name: str
        :return:
            200 - application/json (repository)
            401 - application/json (errors)
            404 - application/json (errors)
        :rtype: requests.Response
        """

        # create BitBucket repo
        url = self.base_http_url + 'rest/api/1.0/projects/' + self.project_key + '/repos/' + repo_name + '/branches'
        headers = {'Content-Type': 'application/json'}
        data = {
            "name": branch_name,
            "startPoint": "master",
            "message": "created dev branch"
        }

        # POST request
        return requests.post(url, auth=self.auth, headers=headers, data=json.dumps(data))

    def get_repo_branches(self, repo_name):
        """Retrieve the branches of the repository.

        This is a paged API. This API can also be invoked via a user-centric URL when addressing repositories in
        personal projects.

        The authenticated user must have REPO_READ permission for the specified repository to call this resource.

        :param repo_name: Name of repository to get branches (i.e. "my_repo").
        :type repo_name: str
        :return:
            200 - application/json (repository)
            401 - application/json (errors)
            404 - application/json (errors)
        :rtype: requests.Response
        """

        # create BitBucket repo
        url = self.base_http_url + 'rest/api/1.0/projects/' + self.project_key + '/repos/' + repo_name + '/branches'
        headers = {'Content-Type': 'application/json'}

        # GET request
        return requests.get(url, auth=self.auth, headers=headers)
