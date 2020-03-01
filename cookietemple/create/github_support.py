from os import path
from subprocess import Popen, PIPE

import click
from github import Github


@click.command()
@click.option('--github_username',  prompt='github username')
@click.option('--github_password',  prompt='github_password', hide_input=True)
@click.option('--private/--public', prompt='private')
def run(github_username, github_password, private):
    # login to github
    authenticated_github_user = Github(github_username, github_password)
    user = authenticated_github_user.get_user()

    is_org: bool = False
    # create the new repository
    if is_org:
        org = authenticated_github_user.get_organization('someorg')
        repo = org.create_repo('projectname', description='somedescription', private=private)
    else:
        repo = user.create_repo('testrepo_github_api', description='this is a test', private=private)

    repository = path.dirname('/tmp/test_clone/')
    git_query = Popen(['/usr/bin/git', 'clone', f'https://{github_username}:{github_password}@github.com/{github_username}/testrepo_github_api', repository],
                      stdout=PIPE, stderr=PIPE, universal_newlines=True)
    (git_status, error) = git_query.communicate()

    # create some dummy data
    with open('/tmp/test_clone/test.txt', 'w') as f:
        f.write('wtf')

    print(f"CLONE: {git_status} ___ {error}")
    git_query = Popen(['git', 'add', '.'],
                      cwd=repository, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    (git_status, error) = git_query.communicate()
    print(f"ADD: {git_status} ___ {error}")
    git_query = Popen(['git', 'commit', '-m', r'"bla"'],
                      cwd=repository, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    (git_status, error) = git_query.communicate()
    print(f"COMMIT: {git_status} ___ {error}")
    git_query = Popen(['git', 'push', '-u', f'https://{github_username}:{github_password}@github.com/{github_username}/testrepo_github_api', '--all'],
                      cwd=repository, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    (git_status, error) = git_query.communicate()
    print(f"PUSH: {git_status} ___ {error}")


if __name__ == '__main__':
    run()
