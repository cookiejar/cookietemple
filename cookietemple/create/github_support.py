import click
import pygit2
from github import Github


@click.command()
@click.option('--github_username',  prompt='github username')
@click.option('--github_password',  prompt='github_password', hide_input=True)
@click.option('--github_email',  prompt='github_email')
def run(github_username, github_password, github_email):
    # login to github
    authenticated_github_user = Github(github_username, github_password)
    user = authenticated_github_user.get_user()

    is_org: bool = False
    # create the new repository
    if is_org:
        org = authenticated_github_user.get_organization('someorg')
        repo = org.create_repo('projectname', description='somedescription')
    else:
        repo = user.create_repo('testrepo_github_api', description='this is a test')

    # clone the repository
    repoClone = pygit2.clone_repository(repo.git_url, '/tmp/test_clone')

    # write a dummy file
    # with open('/tmp/test_clone/test.txt', 'w') as f:
    #     f.write('some_content')

    # create some new files in the repo
    repo.create_file("README.md", "init commit", 'readmeText')

    # Commit it
    repoClone.remotes.set_url("origin", repo.clone_url)
    index = repoClone.index
    index.add_all()
    index.write()
    author = pygit2.Signature("Jesus Christ", github_email)
    commiter = pygit2.Signature("Jesus Christ", github_email)
    tree = index.write_tree()
    try:
        oid = repoClone.create_commit('refs/heads/master', author, commiter, "init commit", tree, [repoClone.head.get_object().hex])
    except pygit2.GitError:
        pass # this occurs, since we do not have a master reference on a fresh, new repository
    remote = repoClone.remotes["origin"]
    credentials = pygit2.UserPass(github_username, github_password)
    remote.credentials = credentials

    callbacks = pygit2.RemoteCallbacks(credentials=credentials)

    # push!
    try:
        remote.push(['refs/heads/master'], callbacks=callbacks)
    except pygit2.GitError:
        pass  # this occurs, since we do not have a master reference on a fresh, new repository


if __name__ == '__main__':
    run()
