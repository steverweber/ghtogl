ghtogl
======

migrate github project issues,notes,milestones,labels to gitlab project

```
usage: ghtogl.py [-h] [-v] [--github_api GITHUB_API]
                 [--github_api_token GITHUB_API_TOKEN] --github_project
                 GITHUB_PROJECT --gitlab_api GITLAB_API --gitlab_api_token
                 GITLAB_API_TOKEN --gitlab_project GITLAB_PROJECT

Migrate issues,comments,labels,milestones from github project to gitlab
project

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  --github_api GITHUB_API
                        Github api
  --github_api_token GITHUB_API_TOKEN
                        api token, https://github.com/settings/applications
                        #personal-access-tokens
  --github_project GITHUB_PROJECT
                        Github project path example: namespace/project
  --gitlab_api GITLAB_API
                        example: https://gitlab.localhost.domain/api/v3
  --gitlab_api_token GITLAB_API_TOKEN
                        get your api token at
                        [https://gitlab.localhost.domain]/profile/account
  --gitlab_project GITLAB_PROJECT
                        getlab project path example: namespace/project
```

