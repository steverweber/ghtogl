import requests

# license = http://opensource.org/licenses/MIT

class Github:
  '''
  NOTE:
  if you perform too many requests to github you will get locked out for 1h
  see: http://developer.github.com/v3/#rate-limiting
  Set api_token to reduce the issue.
  '''
  
  def __init__(self, api_url='https://api.github.com', api_token=None):
    self.api_url = api_url
    self.headers={ 'Accept': 'application/vnd.github.full+json' }
    if api_token:
      self.headers.update({ 'Authorization': 'token ' + api_token})
    self.max_pages = 5
    self.per_page = 90
    
  def get_ratelimit_remaining(self):
    r = requests.get(self.api_url, headers=self.headers)
    return r.headers['x-ratelimit-remaining']

  def get_requests(self):
    return requests.get(self.api_url)
    
  def _get_all_data(self, url, params={}, data=None):
    ## TODO: NOT TESTED WITH LARGE PAGE!!
    out = []
    page = 0
    while page < self.max_pages:
      page += 1
      rparams = {'per_page': self.per_page, 'page': page }
      rparams.update(params)
      r = requests.get(url, data=data, params=rparams, headers=self.headers )
      if r.status_code > 201:
	raise Exception(r.content)
      page_out = r.json()
      out.extend(r.json())
      if len(page_out) < self.per_page:
	break
    return out

  def get_milestones(self, path):
    url = '{0}/repos/{1}/milestones'.format(self.api_url, path)
    return self._get_all_data(url)

  def get_issues_closed(self, path):
    url = '{0}/repos/{1}/issues'.format(self.api_url, path)
    return self._get_all_data(url, params={'state': 'closed'})
  
  def get_issues_open(self, path):
    url = '{0}/repos/{1}/issues'.format(self.api_url, path)
    return self._get_all_data(url, params={'state': 'open'})
  
  def get_issue_comments(self, path, issue_number):
    url = '{0}/repos/{1}/issues/{2}/comments'.format(self.api_url, path, issue_number)
    #GET /repos/:owner/:repo/issues/:number/comments
    return self._get_all_data(url, params={'state': 'open'})


class Gitlab:

  def __init__(self, api_url, api_token):
    '''
    api_url ='https://gitlab.com/api/v3'
    api_token = the token to find under /profile/account
    '''
    self.api_url = api_url
    self.headers={'PRIVATE-TOKEN': api_token}
    self.max_pages = 5
    self.per_page = 90

  def _get_all_data(self, url, params={}, data=None):
    ## TODO: NOT TESTED WITH LARGE PAGE!!
    out = []
    page = 0
    while page < self.max_pages:
      page += 1
      rparams = {'per_page': self.per_page, 'page': page }
      rparams.update(params)
      r = requests.get(url, data=data, params=rparams, headers=self.headers )
      if r.status_code > 201:
	raise Exception(r.content)
      page_out = r.json()
      out.extend(r.json())
      if len(page_out) < self.per_page:
	break
    return out

  def get_projects(self):
    url = '{0}/projects'.format(self.api_url)
    return self._get_all_data(url)


  def get_project(self, path):
    '''
    path is like group.name/projectname
    path includes path_with_namespace!
    '''
    for p in self.get_projects():
      if p['path_with_namespace'] == path:
	return p
    return None
    
  def get_project_id(self, path):
    return self.get_project(path)['id']

  def get_milestones(self, id):
    url = '{0}/projects/{1}/milestones'.format(self.api_url, id)
    return self._get_all_data(url)

  def get_issues(self, id):
    url = '{0}/projects/{1}/issues'.format(self.api_url, id)
    return self._get_all_data(url)
  
  def get_issue_notes(self, id, issue_id):
    url = '{0}/projects/{1}/issues/{2}/notes'.format(self.api_url, id, issue_id)
    return self._get_all_data(url)
  
  def post_issue_note(self, id, issue_id, data={'body':None}):
    '''
    Create issue note
    
    id (required) - The ID of a project
    issue_id (required) - The ID of an issue
    body (required) - The content of a note
    '''
    url = '{0}/projects/{1}/issues/{2}/notes'.format(self.api_url, id, issue_id)
    r = requests.post(url, data=data, headers=self.headers)
    if r.status_code > 201:
      raise Exception(r.content)
    return r.json()

    
  def post_milestone(self, id, data={'title': None, 'description': None}):
    '''
    Create milestone
    
    id (required) - The ID of a project
    title (required) - The title of an milestone
    description (optional) - The description of the milestone
    due_date (optional) - The due date of the milestoneoat
    '''
    url = '{0}/projects/{1}/milestones'.format(self.api_url, id)
    r = requests.post(url, data=data, headers=self.headers)
    if r.status_code > 201:
      raise Exception(r.content)
    return r.json()


  def post_issue(self, id, data={'title': 'None', 'state': 'closed' }):
    '''
    Create issue
    
    id (required) - The ID of a project
    title (required) - The title of an issue
    description (optional) - The description of an issue
    assignee_id (optional) - The ID of a user to assign issue
    milestone_id (optional) - The ID of a milestone to assign issue
    labels (optional) - Comma-separated label names for an issue
    '''
    url = '{0}/projects/{1}/issues'.format(self.api_url, id)
    # headers={'content-type': 'application/json'}
    r = requests.post(url, data=data, headers=self.headers)
    if r.status_code > 201:
      raise Exception(r.content)
    return r.json()


  def put_issue(self, id, issue_id, data={ 'state_event': 'close' }):
    '''
    Edit issue
    
    id (required) - The ID of a project
    issue_id (required) - The ID of a project's issue
    title (optional) - The title of an issue
    description (optional) - The description of an issue
    assignee_id (optional) - The ID of a user to assign issue
    milestone_id (optional) - The ID of a milestone to assign issue
    labels (optional) - Comma-separated label names for an issue
    state_event (optional) - The state event of an issue ('close' to close issue and 'reopen' to reopen it)
    '''
    url = '{0}/projects/{1}/issues/{2}'.format(self.api_url, id, issue_id)
    r = requests.put(url, data=data, headers=self.headers )
    if r.status_code > 201:
      raise Exception(r.content)
    return r.json()


def main(args):
  
  github = Github(args.github_api, args.github_api_token)
  gitlab = Gitlab(args.gitlab_api, args.gitlab_api_token)
  
  gh_m = github.get_milestones(args.github_project)
  gh_i = []
  gh_i.extend(github.get_issues_open(args.github_project))
  gh_i.extend(github.get_issues_closed(args.github_project))
  
  gh_ratelimit_remaining = github.get_ratelimit_remaining()

  print(u'Remaining github {0} API calls'.format(gh_ratelimit_remaining))
  if gh_ratelimit_remaining < 50:
    print(u'WARNING: Github API call limit is low, please check --github_api_token')  
  print(u'Using github project: {0}'.format(args.github_project))
  print(u'Found github milestones: {0}, issues: {1}'.format(len(gh_m), len(gh_i)))

  gl_p = gitlab.get_project(args.gitlab_project)
  pid = gl_p['id']
  # owner id moved https://github.com/steverweber/ghtogl/issues/9
  if 'namespace' in gl_p:
    owner_id = gl_p['namespace']
  if 'owner' in gl_p:
    if 'id' in gl_p['owner']:
      owner_id = gl_p['owner']['id']

  print(u'Using gitlab project: {0}'.format(args.gitlab_project))
  print(u'Found gitlab project_id: {0}, and owner_id: {1}'.format(pid, owner_id))

  milestone_map = {}
  for m in gh_m:
    data={ 'title': m['title'], 'description': m['description'] }
    print(u'Creating gitlab milestone: {0}'.format(m['title']))
    new_m = gitlab.post_milestone(pid, data=data )
    milestone_map[m['id']] = new_m['id']
    
  # reversed order because we want that order in gitlab
  for i in reversed(gh_i):

    data={ 
      'title': i['title'], 
      'assignee_id': owner_id,
    }
    
    if i.get('body',None):
      data['description'] = i['body']
      
    if i.get('labels',None):
      a = []
      for l in i['labels']:
        a.append(l['name'])
      data['labels'] = ",".join(a)
      
    if i.has_key('milestone') and i['milestone']:
      data['milestone_id'] = milestone_map.get(i['milestone']['id'], None)
    
    print(u'Creating gitlab issue: {0}'.format(i['title']))
    new_i = gitlab.post_issue(pid, data=data )
    
    if i['comments'] > 0:
      comments = github.get_issue_comments(args.github_project, i['number'])
      print(u' |- adding comments: {0}'.format(i['comments']))
      for c in comments:
	gitlab.post_issue_note(pid, new_i['id'], data={ 'body': c['body'] } )
      
    if i['state'] == 'closed':
      print(u' |- Update gitlab issue_id: {0} state: {2}'.format(new_i['id'], i['title'], i['state']))
      ## Note: Gitlab uses 'close' not 'closed'
      gitlab.put_issue(pid, new_i['id'], data={ 'state_event': 'close' } )




if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser(description='Migrate issues, comments, labels, and milestones from github project to gitlab project')
  parser.add_argument('--version', action='version', default=argparse.SUPPRESS, version='%(prog)s 1.1')
  parser.add_argument('--github_api', type=str, 
		      default='https://api.github.com', 
		      help='github api url: https://api.github.com')
  parser.add_argument('--github_api_token', type=str, 
		      help='api token, https://github.com/settings/applications#personal-access-tokens')
  parser.add_argument('--github_project', type=str, 
                      required=True,
		      help='github project path example: namespace/project')
  parser.add_argument('--gitlab_api', type=str, 
                      required=True,
		      help='gitlab api url example: https://gitlab.localhost.domain/api/v3')
  parser.add_argument('--gitlab_api_token', type=str, 
                      required=True,
		      help='get your api token at [https://gitlab.localhost.domain]/profile/account')
  parser.add_argument('--gitlab_project', type=str, 
                      required=True,
		      help='getlab project path example: namespace/project')
  
  args = parser.parse_args()
  
  main(args)




