import os

import click
from github import Github
from git import Repo

from cookietemple.create.github_support import handle_pat_authentification

# CONFIG
github_username = 'zethson'
project_slug = 'someweirdrepository'
#####################################


# the personal access token for GitHub
access_token = handle_pat_authentification()

# Login to Github
click.echo(click.style('Logging into Github.', fg='blue'))
authenticated_github_user = Github(access_token)
user = authenticated_github_user.get_user()

# Create new repository
click.echo(click.style('Creating Github repository.', fg='blue'))
repo = user.create_repo(project_slug, private=True)

tmp_project_path = '/tmp/test_pr'
os.mkdir(tmp_project_path)
repository = f'{tmp_project_path}'

# git clone
click.echo(click.style('Cloning empty Github repository.', fg='blue'))
Repo.clone_from(f'https://{github_username}:{access_token}@github.com/{github_username}/{project_slug}', repository)

with open(os.path.join(tmp_project_path, 'someuselessfile'), 'w') as temp_file:
    temp_file.write('YOOO KARL ESS HERE')

# the created projct repository with the copied .git directory
cloned_repo = Repo(path=tmp_project_path)

# git add
click.echo(click.style('Staging template.', fg='blue'))
cloned_repo.git.add(A=True)

# git commit
cloned_repo.index.commit('ADDED SOMETHING I DON T CARE')

click.echo(click.style('Pushing template to Github origin master.', fg='blue'))
cloned_repo.remotes.origin.push(refspec='master:master')

# git create development branch
click.echo(click.style('Creating development branch.', fg='blue'))
cloned_repo.git.checkout('-b', 'development')

# create new file in development
with open(os.path.join(tmp_project_path, 'MORE_USELESS_FILE'), 'w') as temp_file:
    temp_file.write('muschu hassln')

# git add
click.echo(click.style('Staging template.', fg='blue'))
cloned_repo.git.add(A=True)

# git commit
cloned_repo.index.commit('I MADE ALL BASICS')

click.echo(click.style('Pushing template to Github origin development.', fg='blue'))
cloned_repo.remotes.origin.push(refspec='development:development')

# create PR
body = 'this is some PR body'
pr = repo.create_pull(title="Test PR", body=body, head="development", base="master")
