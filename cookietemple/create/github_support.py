import click
import os
import sys
from pathlib import Path
from cryptography.fernet import Fernet
from distutils.dir_util import copy_tree
from subprocess import Popen, PIPE
from github import Github, GithubException
from git import Repo, exc
from ruamel.yaml import YAML

from cookietemple.create.domains.cookietemple_template_struct import CookietempleTemplateStruct
from cookietemple.custom_cli.questionary import cookietemple_questionary
from cookietemple.util.yaml_util import load_yaml_file
from cookietemple.config.config import ConfigCommand


def create_push_github_repository(project_path: str, creator_ctx: CookietempleTemplateStruct, tmp_repo_path: str) -> None:
    """
    Creates a Github repository for the created template and pushes the template to it.
    Prompts the user for the required specifications.

    :param creator_ctx: Full Template Struct. Github username may be updated if an organization repository is warranted.
    :param project_path: The path to the recently created project
    :param tmp_repo_path: Path to the empty cloned repo
    """
    if not is_git_accessible():
        return

    # the personal access token for GitHub
    access_token = handle_pat_authentification()

    # Login to Github
    click.echo(click.style('Logging into Github.', fg='blue'))
    authenticated_github_user = Github(access_token)
    user = authenticated_github_user.get_user()

    # Create new repository
    click.echo(click.style('Creating Github repository.', fg='blue'))
    if creator_ctx.is_github_orga:
        org = authenticated_github_user.get_organization(creator_ctx.github_orga)
        repo = org.create_repo(creator_ctx.project_slug, description=creator_ctx.project_short_description, private=creator_ctx.is_repo_private)
        creator_ctx.github_username = creator_ctx.github_orga
    else:
        repo = user.create_repo(creator_ctx.project_slug, description=creator_ctx.project_short_description, private=creator_ctx.is_repo_private)

    click.echo(click.style('Creating labels and default Github settings.', fg='blue'))
    create_github_labels(repo=repo, labels=[('DEPENDABOT', '1BB0CE')])

    repository = f'{tmp_repo_path}'

    # NOTE: github_username is the organizations name, if an organization repository is to be created

    # git clone
    click.echo(click.style('Cloning empty Github repository.', fg='blue'))
    Repo.clone_from(f'https://{creator_ctx.github_username}:{access_token}@github.com/{creator_ctx.github_username}/{creator_ctx.project_slug}', repository)

    # Copy files which should be included in the initial commit -> basically the template
    copy_tree(f'{repository}', project_path)

    # the created projct repository with the copied .git directory
    cloned_repo = Repo(path=project_path)

    # git add
    click.echo(click.style('Staging template.', fg='blue'))
    cloned_repo.git.add(A=True)

    # git commit
    cloned_repo.index.commit(f'Created {creator_ctx.project_slug} with {creator_ctx.template_handle}'
                             f'template of version {creator_ctx.template_version} using cookietemple.')

    click.echo(click.style('Pushing template to Github origin master.', fg='blue'))
    cloned_repo.remotes.origin.push(refspec='master:master')

    # set branch protection (all WF must pass, dismiss stale PR reviews) only when repo is public
    if not creator_ctx.is_repo_private:
        master_branch = authenticated_github_user.get_user().get_repo(name=creator_ctx.project_slug).get_branch("master")
        master_branch.edit_protection(dismiss_stale_reviews=True)
    else:
        click.echo(click.style('Cannot set branch protection rules due to your repository being private!\n'
                               'You can set it manually later on.', fg='blue'))

    # git create development branch
    click.echo(click.style('Creating development branch.', fg='blue'))
    cloned_repo.git.checkout('-b', 'development')

    # git push to origin development
    click.echo(click.style('Pushing template to Github origin development.', fg='blue'))
    cloned_repo.remotes.origin.push(refspec='development:development')

    # git create TEMPLATE branch
    click.echo(click.style('Creating TEMPLATE branch.', fg='blue'))
    cloned_repo.git.checkout('-b', 'TEMPLATE')

    # git push to TEMPLATE branch
    click.echo(click.style('Pushing template to Github origin TEMPLATE.', fg='blue'))
    cloned_repo.remotes.origin.push(refspec='TEMPLATE:TEMPLATE')

    # checkout to development branch again
    click.echo(click.style('Checkout to development branch.', fg='blue'))
    cloned_repo.git.checkout('development')

    # did any errors occur?
    click.echo(click.style(f'Successfully created a Github repository at https://github.com/{creator_ctx.github_username}/{creator_ctx.project_slug}',
                           fg='green'))


def handle_pat_authentification() -> str:
    """
    Try to read the encrypted Personal Access Token for GitHub.
    If this fails (maybe there was no generated key before) notify user to config its credentials for cookietemple.

    :return: The decrypted PAT
    """

    # check if the key and encrypted PAT already exist
    if os.path.exists(ConfigCommand.CONF_FILE_PATH):
        path = Path(ConfigCommand.CONF_FILE_PATH)
        yaml = YAML(typ='safe')
        settings = yaml.load(path)
        if os.path.exists(ConfigCommand.KEY_PAT_FILE) and 'pat' in settings:
            pat = decrypt_pat()
            return pat
        else:
            click.echo(click.style('Could not find encrypted personal access token!\n', fg='red'))
            click.echo(
                click.style('Please navigate to Github -> Your profile -> Settings -> Developer Settings -> Personal access token -> Generate a new Token',
                            fg='blue'))
            click.echo(click.style('Only tick \'repo\'. The token is a hidden input to cookietemple and stored encrypted locally on your machine.', fg='blue'))
            click.echo(click.style('For more information please read'
                                   ' https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line\n\n',
                                   fg='blue'))
            click.echo(click.style('Lets move on to set your personal access token for your cookietemple project!', fg='blue'))
            # set the PAT
            ConfigCommand.config_pat()
            # if the user wants to create a GitHub repo but accidentally presses no on PAT config prompt
            if not os.path.exists(ConfigCommand.KEY_PAT_FILE):
                click.echo(click.style('No Github personal access token found. Please set it using ', fg='red')
                           + click.style('cookietemple config github', fg='green'))
                sys.exit(1)
            else:
                pat = decrypt_pat()
            return pat
    else:
        click.echo(click.style('Cannot find a cookietemple config file! Did you delete it?', fg='red'))


def prompt_github_repo() -> (bool, bool, bool, str):
    """
    Ask user for all settings needed in order to create and push automatically to GitHub repo.

    :return if is git repo, if repo should be private, if user is an organization and if so, the organizations name
    """
    create_git_repo, private, is_github_org, github_org = False, False, False, ''
    if cookietemple_questionary('confirm', 'Do you want to create a Github repository and push your template to it?', default='Yes'):
        create_git_repo = True
        is_github_org = cookietemple_questionary('confirm', 'Do you want to create an organization repository?', default='No')
        github_org = cookietemple_questionary('text',
                                              'Please enter the name of the Github organization',
                                              default='SpringfieldNuclearPowerPlant') if is_github_org else ''
        private = cookietemple_questionary('confirm', 'Do you want your repository to be private?', default='No')

    return create_git_repo, private, is_github_org, github_org


def decrypt_pat() -> str:
    """
    Decrypt the encrypted PAT.

    :return: The decrypted Personal Access Token for GitHub
    """
    # read key and encrypted PAT from files
    with open(ConfigCommand.KEY_PAT_FILE, 'rb') as f:
        key = f.readline()
    fer = Fernet(key)
    encrypted_pat = load_yaml_file(ConfigCommand.CONF_FILE_PATH)['pat']
    # decrypt the PAT and decode it to string
    click.echo(click.style('Decrypting personal access token.', fg='blue'))
    decrypted_pat = fer.decrypt(encrypted_pat).decode('utf-8')

    return decrypted_pat


def load_github_username() -> str:
    """
    Load the username from cfg file.

    :return: The users Github account name
    """
    return load_yaml_file(ConfigCommand.CONF_FILE_PATH)['github_username']


def is_git_accessible() -> bool:
    """
    Verifies that git is accessible and in the PATH.

    :return: True if accessible, false if not
    """
    git_installed = Popen(['git', '--version'], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    (git_installed_stdout, git_installed_stderr) = git_installed.communicate()
    if git_installed.returncode != 0:
        click.echo(click.style('Could not find \'git\' in the PATH. Is it installed?', fg='red'))
        click.echo(click.style('Run command was: \'git --version \'', fg='red'))
        return False

    return True


def create_github_labels(repo, labels: list) -> None:
    """
    Create github labels and add them to the repository.
    If failed, print error message.

    :param repo: The repository where the label needs to be added
    :param labels: A list of the new labels to be added
    """
    for label in labels:
        try:
            repo.create_label(name=label[0], color=label[1])
        except GithubException:
            click.echo(click.style(f'Unable to create label {label[0]} due to permissions', fg='red'))


def is_git_repo(path: Path) -> bool:
    """
    Check if directory is a git repo

    :param path: The directory to check
    :return: true if path is git repo false otherwise
    """
    try:
        _ = Repo(path).git_dir
        return True
    except exc.InvalidGitRepositoryError:
        return False
