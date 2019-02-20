import requests
import json
import ntpath


class Jira:
    """

    """

    def __init__(self, base_http_url, project_key, auth):
        self.base_http_url = base_http_url
        self.project_key = project_key
        self.auth = auth

    def create_issue(self, summary, description='', issue_type='Task'):
        """Create Issue in Jira

        Create issue with summary, description, and issue type.

        :param summary: A brief summary of the issue. This will be the "title" shown next to the issue id on the boards.
        :type summary: str
        :param description: More details about the issue.
        :type description: str
        :param issue_type: Choose one of the predefined issue types for your project ('Bug', 'Task', 'Story', and
            'Epic' by default.)
        :type issue_type: str
        :return: Response from the POST request.
            STATUS 201: Success - application/json Returns a link to the created issue. \n
            STATUS 400: Error - STATUS 400Returned if the input is invalid (e.g. missing required fields, invalid
                        field values, and so forth).
        :rtype: list[requests.Response, str]
        """

        # create Jira issue
        url = self.base_http_url + 'rest/api/2/issue'
        headers = {'Content-Type': 'application/json'}
        data = {
            "fields": {
                "project": {
                    "key": self.project_key
                },
                "summary": summary,
                "description": description,
                "issuetype": {
                    "name": issue_type
                }
            }
        }

        r = requests.post(url, auth=self.auth, headers=headers, data=json.dumps(data))
        print(json.dumps(data))
        print(r.status_code)
        print(r.text)
        return r

    def get_issues(self, issue_id=None, max_results=10, start_at=0):
        """Get specific or list of Jira issue(s).

        Get specific issue by setting the issue_id. Get a list of issues by leaving the issue_id blank and setting the
        limit for the pagination size (default=10).

        :param issue_id: JIRA will attempt to identify the issue by the issueIdOrKey path parameter. This can be an
            issue id, or an issue key.
        :type issue_id: str
        :param max_results: The "maxResults" parameter indicates how many results to return per page.
        :type max_results: int
        :param start_at: The "startAt" parameter indicates which item should be used as the first item in the page of
            results.
        :type start_at: int
        :return:
            STATUS 200: Success - application/jsonReturns a full representation of a JIRA issue in JSON format.
            STATUS 404: Error - Returned if the requested issue is not found, or the user does not have permission to
                        view it.
        :rtype: list[requests.Response, str]
        """

        if issue_id is None:
            url = self.base_http_url + 'rest/api/2/issue?maxResults=' + str(max_results) + '&startAt' + str(start_at)
        else:
            url = self.base_http_url + 'rest/api/2/issue/' + str(issue_id)
        headers = {'Content-Type': 'application/json'}

        r = requests.get(url, auth=self.auth, headers=headers)
        print(r.status_code)
        print(r.text)
        return r

    def add_attachment(self, issue_id, attachments):
        """Add attachments to Jira issue

        :param issue_id: JIRA will attempt to identify the issue by the issueIdOrKey path parameter. This can be an
            issue id, or an issue key.
        :type issue_id: str
        :param attachments: List of string paths to attachments to be uploaded and added to an issue.
        :type attachments: list[str]
        :return:
            STATUS 200: Success - application/json
            STATUS 403: Error - Returned if attachments is disabled or if you don't have permission to add attachments
                        to this issue.
            STATUS 404: Error - Returned if the requested issue is not found, the user does not have permission to
                        view it, or if the attachments exceeds the maximum configured attachment size.
        :rtype: list[requests.Response, str]
        """

        # add attachments to Jira issue
        url = self.base_http_url + 'rest/api/2/issue/' + issue_id + '/attachments'
        headers = {'X-Atlassian-Token': 'no-check'}

        r = []
        filenames = []

        # POST request for attachments
        if attachments:
            for file in attachments:
                upload = open(file, 'rb')
                filenames.append(ntpath.basename(file))
                r.append(requests.post(url, auth=self.auth, headers=headers, files={'file': upload}))
                upload.close()
        else:
            r.append('ERROR: No attachments to add.')

        # verify attachments were attached
        if attachments:
            jira_attachments = self.get_issues(issue_id).json()['fields']['attachment']

            for filename in filenames:
                if not any(d['filename'] == filename for d in jira_attachments):
                    # does not exist
                    r.append('ERROR: File ' + filename + ' was not attached.')
        return r
