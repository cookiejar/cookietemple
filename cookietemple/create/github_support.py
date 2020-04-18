import click
import os

from cryptography.fernet import Fernet
from distutils.dir_util import copy_tree
from subprocess import Popen, PIPE
from github import Github, GithubException
from git import Repo
from pathlib import Path


def create_push_github_repository(project_name: str, project_description: str, template_creation_path: str) -> None:
    """
    Creates a Github repository for the created template and pushes the template to it.
    Prompts the user for the required specifications.

    :param project_name: Name of the created project
    :param project_description: Description of the created project
    :param template_creation_path: Path to the already created template
    """
    if not is_git_accessible():
        return

    # Prompt for Github username, organization name if wished and whether private repository
    github_username: str = click.prompt('Please enter your Github account username: ',
                                        type=str)
    # the personal access token for GitHub
    access_token = handle_pat_authentification()

    is_github_org: bool = click.prompt('Do you want to create an organization repository? [y, n]',
                                       type=bool,
                                       default='No')
    if is_github_org:
        github_org: str = click.prompt('Please enter the name of the Github organization: ',
                                       type=str)
    private: bool = click.prompt('Do you want your repository to be private?  [y, n]',
                                 type=bool,
                                 default='No')

    # Login to Github
    click.echo(click.style('Logging into Github.', fg='blue'))
    authenticated_github_user = Github(access_token)
    user = authenticated_github_user.get_user()

    # Create new repository
    click.echo(click.style('Creating Github repository.', fg='blue'))
    if is_github_org:
        org = authenticated_github_user.get_organization(github_org)
        repo = org.create_repo(project_name, description=project_description, private=private)
        github_username = github_org
    else:
        repo = user.create_repo(project_name, description=project_description, private=private)

    click.echo(click.style('Creating labels and default Github settings.', fg='blue'))
    create_dependabot_label(repo=repo, name="DEPENDABOT")

    repository = f'{os.getcwd()}/{project_name}'

    # NOTE: github_username is the organizations name, if an organization repository is to be created

    # git clone
    click.echo(click.style('Cloning empty Github repoitory.', fg='blue'))
    cloned_repo = Repo.clone_from(f'https://{github_username}:{access_token}@github.com/{github_username}/{project_name}', repository)

    # Copy files which should be included in the initial commit -> basically the template
    copy_tree(template_creation_path, repository)

    # git add
    click.echo(click.style('Staging template.', fg='blue'))
    cloned_repo.git.add(A=True)

    # git commit
    cloned_repo.index.commit('Initial commit')

    click.echo(click.style('Pushing template to Github origin master.', fg='blue'))
    cloned_repo.remotes.origin.push(refspec='master:master')

    # git create development branch
    click.echo(click.style('Creating development branch.', fg='blue'))
    cloned_repo.git.checkout('-b', 'development')

    # git push to origin development
    click.echo(click.style('Pushing template to Github origin development.', fg='blue'))
    cloned_repo.remotes.origin.push(refspec='development:development')

    # did any errors occur?
    click.echo(click.style(f'Successfully created a Github repository at https://github.com/{github_username}/{project_name}', fg='green'))


def handle_pat_authentification() -> str:
    """
    Try to read the encrypted Personal Acess Token for GitHub.
    If this fails (maybe there was no generated key before) then encrypt and return the PAT afterwards.
    :return: The decrypted PAT
    """

    # check if the key and encrypted PAT already exist
    if os.path.exists(f'{Path.home()}/.ct_keys') and os.path.exists(f'{Path.home()}/cookietemple_conf'):
        pat = decrypt_pat()
        return pat

    else:
        click.echo(click.style("Could not read key from ~/cookietemple_conf!", fg='red'))
        click.echo()
        click.echo(click.style('Please navigate to Github -> Your profile -> Developer Settings -> Personal access token -> Generate a new Token', fg='blue'))
        click.echo(click.style('Please only tick \'repo\'. Note that the token is a hidden input to COOKIETEMPLE.', fg='blue'))
        click.echo(click.style('For more information please read'
                               ' https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line', fg='blue'))
        access_token: str = click.prompt('Please enter your GitHub access token: ',
                                         type=str,
                                         hide_input=True)
        access_token_b = access_token.encode('utf-8')

        # encrypt the given PAT and save the encryption key and encrypted PAT in separate files
        key = Fernet.generate_key()
        fer = Fernet(key)
        encrypted_pat = fer.encrypt(access_token_b)

        with open(f'{Path.home()}/cookietemple_conf', 'wb') as f:
            f.write(encrypted_pat)

        with open(f'{Path.home()}/.ct_keys', 'wb') as f:
            f.write(key)

        pat = decrypt_pat()
        return pat


def decrypt_pat() -> str:
    """
    Decrypt the encrypted PAT.
    :return: The decrypted Personal Access Token for GitHub
    """

    # read key and encrypted PAT from files
    with open(f'{Path.home()}/.ct_keys', 'rb') as f:
        key = f.readline()

    with open(f'{Path.home()}/cookietemple_conf', 'rb') as f:
        encrypted_pat = f.readline()

    fer = Fernet(key)

    # decrypt the PAT and decode it to string
    decrypted_pat = fer.decrypt(encrypted_pat).decode('utf-8')

    return decrypted_pat


def is_git_accessible() -> bool:
    """
    Verifies that git is accessible and in the PATH.

    :return: True if accessible, false if not
    """
    git_installed = Popen(['git', '--version'], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    (git_installed_stdout, git_installed_stderr) = git_installed.communicate()
    if git_installed.returncode != 0:
        click.echo(click.style(f'Could not find \'git\' in the PATH. Is it installed?', fg='red'))
        click.echo(click.style('Run command was: git', fg='red'))
        return False

    return True


def create_dependabot_label(repo, name: str) -> None:
    """
    Create a dependabot label and add it to the repository.
    If failed, print error message.
    :param repo: The repository where the label needs to be added
    :param name: The name of the new label
    """
    try:
        repo.create_label(name=name, color="1BB0CE")
    except GithubException:
        click.echo(click.style("Unable to create label {} due to permissions".format(name), fg='red'))
