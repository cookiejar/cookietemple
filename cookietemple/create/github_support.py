from collections import OrderedDict

import click
import os
import sys
import requests
import json
from base64 import b64encode
from nacl import encoding, public
from pathlib import Path
from cryptography.fernet import Fernet
from distutils.dir_util import copy_tree
from subprocess import Popen, PIPE
from github import Github, GithubException
from git import Repo, exc
from ruamel.yaml import YAML

from cookietemple.create.domains.cookietemple_template_struct import CookietempleTemplateStruct
from cookietemple.custom_cli.questionary import cookietemple_questionary_or_dot_cookietemple
from cookietemple.common.load_yaml import load_yaml_file
from cookietemple.config.config import ConfigCommand


def create_push_github_repository(project_path: str, creator_ctx: CookietempleTemplateStruct, tmp_repo_path: str) -> None:
    """
    Creates a Github repository for the created template and pushes the template to it.
    Prompts the user for the required specifications.

    :param creator_ctx: Full Template Struct. Github username may be updated if an organization repository is warranted.
    :param project_path: The path to the recently created project
    :param tmp_repo_path: Path to the empty cloned repo
    """
    try:
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

        # create the repos sync secret
        click.echo(click.style('Creating your repositories sync secret.', fg='blue'))
        create_sync_secret(creator_ctx.github_username, creator_ctx.project_slug, access_token, creator_ctx.is_github_orga, creator_ctx.github_orga)

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
        if not creator_ctx.is_repo_private and not creator_ctx.is_github_orga:
            master_branch = authenticated_github_user.get_user().get_repo(name=creator_ctx.project_slug).get_branch("master")
            master_branch.edit_protection(dismiss_stale_reviews=True)
        else:
            click.echo(click.style('Cannot set branch protection rules due to your repository being private or an orga repo!\n'
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
    except (GithubException, ConnectionError) as e:
        handle_failed_github_repo_creation(e)


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


def prompt_github_repo(dot_cookietemple: OrderedDict or None) -> (bool, bool, bool, str):
    """
    Ask user for all settings needed in order to create and push automatically to GitHub repo.

    :param dot_cookietemple: .cookietemple.yml content if passed
    :return if is git repo, if repo should be private, if user is an organization and if so, the organizations name
    """
    # if dot_cookietemple dict was passed -> return the Github related properties and do NOT prompt for them
    try:
        if dot_cookietemple:
            if not dot_cookietemple['is_github_orga']:
                return dot_cookietemple['is_github_repo'], dot_cookietemple['is_repo_private'], 'false', ''
            else:
                return dot_cookietemple['is_github_repo'], dot_cookietemple['is_repo_private'], dot_cookietemple['is_github_orga'], \
                       dot_cookietemple['github_orga']
    except KeyError:
        click.echo(click.style('Missing required Github properties in .cookietemple.yml file!', fg='red'))

    # No dot_cookietemple_dict was passed -> prompt whether to create a Github repository and the required settings
    create_git_repo, private, is_github_org, github_org = False, False, False, ''
    if cookietemple_questionary_or_dot_cookietemple(function='confirm',
                                                    question='Do you want to create a Github repository and push your template to it?',
                                                    default='Yes'):
        create_git_repo = True
        is_github_org = cookietemple_questionary_or_dot_cookietemple(function='confirm',
                                                                     question='Do you want to create an organization repository?',
                                                                     default='No')
        github_org = cookietemple_questionary_or_dot_cookietemple(function='text',
                                                                  question='Please enter the name of the Github organization',
                                                                  default='SpringfieldNuclearPowerPlant') if is_github_org else ''
        private = cookietemple_questionary_or_dot_cookietemple(function='confirm',
                                                               question='Do you want your repository to be private?',
                                                               default='No')

    return create_git_repo, private, is_github_org, github_org


def create_sync_secret(username: str, repo_name: str, token: str, is_orga: bool, orga_name: str) -> None:
    """
    Create the secret cookietemple uses to sync repos. The secret contains the personal access token with the repo scope.
    NOTE: IF YOU ONE WANTS TO CREATE AN ORGA REPO THE PAT MUST HAVE ADDITIONALLY THE ADMIN:ORG SCOPE!!!!
    Following steps are required (PAT MUST have at least repo access):
    1.) Get the repos public key (and its ID) which is needed for secret's value (PAT) encryption; for private repos especially we need an authentification
        header for a successful request.
    2.) Encrypt the secret value using PyNacl (a Python binding for Javascripts LibSodium) and send the data with an authentification header (PAT) and the
        public key's ID via PUT to the Github API.

    :param username: The users github username
    :param repo_name: The repositories name
    :param token: The PAT of the user with repo scope
    :param orga_name: Name of the orga (if any)
    :param is_orga: Whether the repo is created within an orga
    """
    public_key_dict = get_repo_public_key(username, repo_name, token, is_orga, orga_name)
    create_secret(username, repo_name, token, public_key_dict['key'], public_key_dict['key_id'], is_orga, orga_name)


def get_repo_public_key(username: str, repo_name: str, token: str, is_orga: bool, orga_name: str) -> dict:
    """
    Get the public key for a repository via the Github API. At least for private repos, a personal access token (PAT) with the repo scope is required.
    NOTE: IF YOU ONE WANTS TO CREATE AN ORGA REPO THE PAT MUST HAVE ADDITIONALLY THE ADMIN:ORG SCOPE!!!!

    :param username: The users github username
    :param repo_name: The repositories name
    :param token: The PAT of the user with repo scope
    :param is_orga: If the repo is created in an orga
    :param orga_name: Name of the orga (if any)
    :return: A dict containing the public key and its ID
    """
    query_url = f'https://api.github.com/repos/{username}/{repo_name}/actions/secrets/public-key' if not is_orga else \
        f'https://api.github.com/orgs/{orga_name}/actions/secrets/public-key'
    headers = {'Authorization': f'token {token}'}
    r = requests.get(query_url, headers=headers)
    return r.json()


def create_secret(username: str, repo_name: str, token: str, public_key_value: str, public_key_id: str, is_orga: bool, orga_name: str) -> None:
    """
    Create the secret named CT_SYNC_TOKEN using a PUT request via the Github API. This request needs a PAT with the repo scope for authentification purposes.
    Using PyNacl, a Python binding for Javascripts LibSodium, it encrypts the secret value, which is required by the Github API.
    NOTE: IF YOU ONE WANTS TO CREATE AN ORGA REPO THE PAT MUST HAVE ADDITIONALLY THE ADMIN:ORG SCOPE!!!!

    :param username: The user's github username
    :param repo_name: The repositories name
    :param token: The PAT of the user with repo scope
    :param public_key_value: The public keys value (the key) of the repos public key PyNacl uses for encryption of the secrets value
    :param public_key_id: The ID of the public key used for encryption
    :param is_orga: Whether the repo is created within an orga
    :param orga_name: Name of the orga (if any)
    """
    encrypted_value = encrypt_sync_secret(public_key_value, token)
    # the parameters required by the Github API
    params = {
        "encrypted_value": encrypted_value,
        "key_id": public_key_id
    } if not is_orga else {
        "encrypted_value": encrypted_value,
        "key_id": public_key_id,
        "visibility": "selected",
        "selected_repository_ids": [get_orga_repo_id(orga_name, repo_name, token)]
    }
    # the authentification header
    headers = {'Authorization': f'token {token}'}
    # the url used for PUT
    # TODO: ADD CHECK SO THAT TOKEN WILL NOT BE OVERWRITTEN IN ORGA IF TWO USER CREATE PROJECT WITHIN THAT ORGA (NECESSARY???)
    put_url = f'https://api.github.com/repos/{username}/{repo_name}/actions/secrets/CT_SYNC_TOKEN' if not is_orga else \
        f'https://api.github.com/orgs/{orga_name}/actions/secrets/CT_SYNC_TOKEN'
    requests.put(put_url, headers=headers, data=json.dumps(params))


def get_orga_repo_id(orga_name: str, repo_name: str, token: str) -> str:
    """
    Get the ID for the repo in the github orga to set a sync secret for.
    NOTE: This needs a token with repo AND, more important, admin:org scope!

    :param orga_name: Name of the orga
    :param token: PAT of the user
    :param repo_name: Name of the repo in that orga a secret needs to be created for
    :return: The ID of the orga repo
    """
    query_url = f'https://api.github.com/orgs/{orga_name}/repos'
    headers = {'Authorization': f'token {token}'}
    r = requests.get(query_url, headers=headers)
    json_content = r.json()
    for repo in json_content:
        if repo['name'] == repo_name:
            return repo['id']


def encrypt_sync_secret(public_key: str, token: str) -> str:
    """
    Encrypt the sync secret (which is the PAT).

    :param public_key: Public key of the repo we want to create a secret for
    :param token: The users PAT with repo scope as the secret
    :return: The encrypted secret (PAT)
    """
    """Encrypt a Unicode string using the public key."""
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(token.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")


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


def handle_failed_github_repo_creation(e: ConnectionError or GithubException) -> None:
    """
    Called, when the automatic GitHub repo creation process failed during the create process. As this may have various issue sources,
    try to provide the user a detailed error message for the individual exception and inform them about what they should/can do next.

    :param e: The exception that has been thrown
    """
    # output the error dict thrown by PyGitHub due to an error related to GitHub
    if isinstance(e, GithubException):
        click.echo(click.style('\nError while trying to create a Github repo due to an error related to Github API. See below output for detailed information!'
                               '\n', fg='red'))
        format_github_exception(e.data)
    # output an error that might occur due to a missing internet connection
    elif isinstance(e, ConnectionError):
        click.echo(click.style('Error while trying to establish a connection to github.com. Do you have an active internet connection?', fg='red'))


def format_github_exception(data: dict) -> None:
    """
    Format the github exception thrown by PyGitHub in a nice way and output it.

    :param data: The exceptions data as a dict
    """
    for k, v in data.items():
        if not isinstance(v, list):
            click.echo(click.style(f'{k.capitalize()}: {v}', fg='red'))
        else:
            click.echo(click.style(f'{k.upper()}: ', fg='red'))
            messages = [val if not isinstance(val, dict) and not isinstance(val, set) else github_exception_dict_repr(val) for val in v]
            click.echo(click.style('\n'.join(msg for msg in messages), fg='red'))


def github_exception_dict_repr(messages: dict) -> str:
    """
    String representation for Github exception dict thrown by PyGitHub.

    :param messages: The messages as a dict
    """
    return '\n'.join(f'    {k.capitalize()}: {v}' for k, v in messages.items())


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
