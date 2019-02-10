## Setup

Add the following to ```settings.py```:

```
ATLASSIAN_SETTINGS = {
    'jira': {
        'url': 'your_url',
        'username': 'your_username',
        'password': 'your_password'
    },
    'bitbucket': {
        'http_url': 'your_url',   # HTTP address
        'ssh_url': 'your_url',   # SSH address
        'username': 'your_username',
        'password': 'your_password'
    }
}
```


To disable (or control disabling), add the following lines to the beginning of /etc/ssh/ssh_config...

```
Host 192.168.0.*
   StrictHostKeyChecking=no
   UserKnownHostsFile=/dev/null
```
   
Options:

* The Host subnet can be * to allow unrestricted access to all IPs.
* Edit /etc/ssh/ssh_config for global configuration or ~/.ssh/config for user-specific configuration.

## Usage

### Create Repository

```create_repo(uploaded_file_path, project_id, repo_slug)```


### Branch Repository

```branch_repo(project_id, repo_slug, 'test_branch')```


### Create Jira Issue

