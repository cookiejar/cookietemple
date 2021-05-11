import json
import logging
import os
import sys
from base64 import b64encode
from distutils.dir_util import copy_tree
from pathlib import Path
from subprocess import PIPE, Popen
from typing import Any, Dict, Optional, Set, Tuple, Union

import requests
from cryptography.fernet import Fernet
from git import Repo, exc
from github import Github, GithubException
from nacl import encoding, public
from ruamel.yaml import YAML

from cookietemple.common.load_yaml import load_yaml_file
from cookietemple.config.config import ConfigCommand
from cookietemple.create.domains.cookietemple_template_struct import CookietempleTemplateStruct
from cookietemple.custom_cli.questionary import cookietemple_questionary_or_dot_cookietemple
from cookietemple.util.rich import console

log = logging.getLogger(__name__)


def create_push_github_repository(
    project_path: str, creator_ctx: CookietempleTemplateStruct, tmp_repo_path: str
) -> None:
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
        log.debug("Logging into Github.")
        console.print("[bold blue]Logging into Github")
        authenticated_github_user = Github(access_token)
        user = authenticated_github_user.get_user()

        # Create new repository
        console.print("[bold blue]Creating Github repository")
        if creator_ctx.is_github_orga:
            log.debug(f"Creating a new Github repository for organizaton: {creator_ctx.github_orga}.")
            org = authenticated_github_user.get_organization(creator_ctx.github_orga)
            repo = org.create_repo(
                creator_ctx.project_slug,
                description=creator_ctx.project_short_description,  # type: ignore
                private=creator_ctx.is_repo_private,
            )
            creator_ctx.github_username = creator_ctx.github_orga
        else:
            log.debug(f"Creating a new Github repository for user: {creator_ctx.github_username}.")
            repo = user.create_repo(
                creator_ctx.project_slug,
                description=creator_ctx.project_short_description,  # type: ignore
                private=creator_ctx.is_repo_private,
            )

        console.print("[bold blue]Creating labels and default Github settings")
        create_github_labels(repo=repo, labels=[("DEPENDABOT", "1BB0CE")])

        repository = f"{tmp_repo_path}"

        # NOTE: github_username is the organizations name, if an organization repository is to be created

        # create the repos sync secret
        console.print("[bold blue]Creating repository sync secret")
        create_sync_secret(creator_ctx.github_username, creator_ctx.project_slug, access_token)

        # git clone
        console.print("[bold blue]Cloning empty Github repository")
        log.debug(f"Cloning repository {creator_ctx.github_username}/{creator_ctx.project_slug}")
        Repo.clone_from(
            f"https://{creator_ctx.github_username}:{access_token}@github.com/{creator_ctx.github_username}/{creator_ctx.project_slug}",
            repository,
        )

        log.debug("Copying files from the template into the cloned repository.")
        # Copy files which should be included in the initial commit -> basically the template
        copy_tree(f"{repository}", project_path)

        # the created project repository with the copied .git directory
        cloned_repo = Repo(path=project_path)

        # git add
        log.debug("git add")
        console.print("[bold blue]Staging template")
        cloned_repo.git.add(A=True)

        # git commit
        log.debug("git commit")
        cloned_repo.index.commit(
            f"Created {creator_ctx.project_slug} with {creator_ctx.template_handle} "
            f'template of version {creator_ctx.template_version.replace("# <<COOKIETEMPLE_NO_BUMP>>", "")} using cookietemple.'
        )

        # get the default branch of the repository as default branch of GitHub repositories are nor configurable by the user and can be set to any branch name
        # but cookietemple needs to know which one is the default branch in order to push to the correct remote branch and rename local branch, if necessary
        headers = {"Authorization": f"token {access_token}"}
        url = f"https://api.github.com/repos/{creator_ctx.github_username}/{creator_ctx.project_slug}"
        response = requests.get(url, headers=headers).json()
        default_branch = response["default_branch"]
        log.debug(f"git push origin {default_branch}")
        console.print(f"[bold blue]Pushing template to Github origin {default_branch}")
        if default_branch != "master":
            cloned_repo.git.branch("-M", f"{default_branch}")
        cloned_repo.remotes.origin.push(refspec=f"{default_branch}:{default_branch}")

        # set branch protection (all WF must pass, dismiss stale PR reviews) only when repo is public
        log.debug("Set branch protection rules.")

        if not creator_ctx.is_repo_private and not creator_ctx.is_github_orga:
            main_branch = (
                authenticated_github_user.get_user()
                .get_repo(name=creator_ctx.project_slug)
                .get_branch(f"{default_branch}")
            )
            main_branch.edit_protection(dismiss_stale_reviews=True)
        else:
            console.print(
                "[bold blue]Cannot set branch protection rules due to your repository being private or an organization repo!\n"
                "You can set them manually later on."
            )

        # git create development branch
        log.debug("git checkout -b development")
        console.print("[bold blue]Creating development branch.")
        cloned_repo.git.checkout("-b", "development")

        # git push to origin development
        log.debug("git push origin development")
        console.print("[bold blue]Pushing template to Github origin development.")
        cloned_repo.remotes.origin.push(refspec="development:development")

        # git create TEMPLATE branch
        log.debug("git checkout -b TEMPLATE")
        console.print("[bold blue]Creating TEMPLATE branch.")
        cloned_repo.git.checkout("-b", "TEMPLATE")

        # git push to origin TEMPLATE
        log.debug("git push origin TEMPLATE")
        console.print("[bold blue]Pushing template to Github origin TEMPLATE.")
        cloned_repo.remotes.origin.push(refspec="TEMPLATE:TEMPLATE")

        # finally, checkout to development branch
        log.debug("git checkout development")
        console.print("[bold blue]Checking out development branch.")
        cloned_repo.git.checkout("development")

        # did any errors occur?
        console.print(
            f"[bold green]Successfully created a Github repository at https://github.com/{creator_ctx.github_username}/{creator_ctx.project_slug}"
        )

    except (GithubException, ConnectionError) as e:
        handle_failed_github_repo_creation(e)


def handle_pat_authentification() -> str:
    """
    Try to read the encrypted Personal Access Token for GitHub.
    If this fails (maybe there was no generated key before) notify user to config its credentials for cookietemple.

    :return: The decrypted PAT
    """
    # check if the key and encrypted PAT already exist
    log.debug(f"Attempting to read the personal access token from {ConfigCommand.CONF_FILE_PATH}")
    if os.path.exists(ConfigCommand.CONF_FILE_PATH):
        path = Path(ConfigCommand.CONF_FILE_PATH)
        yaml = YAML(typ="safe")
        settings = yaml.load(path)
        if os.path.exists(ConfigCommand.KEY_PAT_FILE) and "pat" in settings:
            pat = decrypt_pat()
            return pat
        else:
            log.debug(f"Unable to read the personal access token from {ConfigCommand.CONF_FILE_PATH}")
            console.print("[bold red]Could not find encrypted personal access token!\n")
            console.print(
                "[bold blue]Please navigate to Github -> Your profile -> Settings -> Developer Settings -> Personal access token -> "
                "Generate a new Token"
            )
            console.print(
                "[bold blue]Only tick 'repo'. The token is a hidden input to cookietemple and stored encrypted locally on your machine."
            )
            console.print(
                "[bold blue]For more information please read"
                + "https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line\n\n"
            )
            console.print("[bold blue]Lets move on to set your personal access token for your cookietemple project!")
            # set the PAT
            ConfigCommand.config_pat()
            # if the user wants to create a GitHub repo but accidentally presses no on PAT config prompt
            if not os.path.exists(ConfigCommand.KEY_PAT_FILE):
                console.print(
                    "[bold red]No Github personal access token found. Please set it using [green]cookietemple config github"
                )
                sys.exit(1)
            else:
                pat = decrypt_pat()
            return pat
    else:
        console.print("[bold red]Cannot find a cookietemple config file! Did you delete it?")

    return ""


def prompt_github_repo(dot_cookietemple: Optional[dict]) -> Tuple[bool, bool, bool, str]:
    """
    Ask user for all settings needed in order to create and push automatically to GitHub repo.

    :param dot_cookietemple: .cookietemple.yml content if passed
    :return if is git repo, if repo should be private, if user is an organization and if so, the organizations name
    """
    # if dot_cookietemple dict was passed -> return the Github related properties and do NOT prompt for them
    try:
        if dot_cookietemple:
            if not dot_cookietemple["is_github_orga"]:
                return dot_cookietemple["is_github_repo"], dot_cookietemple["is_repo_private"], False, ""
            else:
                return (
                    dot_cookietemple["is_github_repo"],
                    dot_cookietemple["is_repo_private"],
                    dot_cookietemple["is_github_orga"],
                    dot_cookietemple["github_orga"],
                )
    except KeyError:
        console.print("[bold red]Missing required Github properties in .cookietemple.yml file!")

    # No dot_cookietemple_dict was passed -> prompt whether to create a Github repository and the required settings
    create_git_repo, private, is_github_org, github_org = False, False, False, ""
    console.print(
        "[bold blue]Automatically creating a Github repository with cookietemple is strongly recommended. "
        "Otherwise you will not be able to use all of cookietemple's features!\n"
    )

    if cookietemple_questionary_or_dot_cookietemple(
        function="confirm",
        question="Do you want to create a Github repository and push your template to it?",
        default="Yes",
    ):
        create_git_repo = True
        is_github_org = cookietemple_questionary_or_dot_cookietemple(
            function="confirm",  # type: ignore
            question="Do you want to create an organization repository?",
            default="No",
        )
        github_org = (
            cookietemple_questionary_or_dot_cookietemple(
                function="text",  # type: ignore
                question="Please enter the name of the Github organization",
                default="SpringfieldNuclearPowerPlant",
            )
            if is_github_org
            else ""
        )
        private = cookietemple_questionary_or_dot_cookietemple(
            function="confirm", question="Do you want your repository to be private?", default="No"  # type: ignore
        )
    return create_git_repo, private, is_github_org, github_org


def create_sync_secret(username: str, repo_name: str, token: Union[str, bool]) -> None:
    """
    Create the secret cookietemple uses to sync repos. The secret contains the personal access token with the repo scope.
    Following steps are required (PAT MUST have at least repo access):
    1.) Get the repos public key (and its ID) which is needed for secret's value (PAT) encryption; for private repos especially we need an authentification
        header for a successful request.
    2.) Encrypt the secret value using PyNacl (a Python binding for Javascripts LibSodium) and send the data with an authentification header (PAT) and the
        public key's ID via PUT to the Github API.

    :param username: The users github username
    :param repo_name: The repositories name
    :param token: The PAT of the user with repo scope
    """
    public_key_dict = get_repo_public_key(username, repo_name, token)
    create_secret(username, repo_name, token, public_key_dict["key"], public_key_dict["key_id"])


def get_repo_public_key(username: str, repo_name: str, token: Union[str, bool]) -> dict:
    """
    Get the public key for a repository via the Github API. At least for private repos, a personal access token (PAT) with the repo scope is required.

    :param username: The users github username
    :param repo_name: The repositories name
    :param token: The PAT of the user with repo scope
    :return: A dict containing the public key and its ID
    """
    query_url = f"https://api.github.com/repos/{username}/{repo_name}/actions/secrets/public-key"
    headers = {"Authorization": f"token {token}"}
    r = requests.get(query_url, headers=headers)

    return r.json()


def create_secret(
    username: str, repo_name: str, token: Union[str, bool], public_key_value: str, public_key_id: str
) -> None:
    """
    Create the secret named CT_SYNC_TOKEN using a PUT request via the Github API. This request needs a PAT with the repo scope for authentification purposes.
    Using PyNacl, a Python binding for Javascripts LibSodium, it encrypts the secret value, which is required by the Github API.

    :param username: The user's github username
    :param repo_name: The repositories name
    :param token: The PAT of the user with repo scope
    :param public_key_value: The public keys value (the key) of the repos public key PyNacl uses for encryption of the secrets value
    :param public_key_id: The ID of the public key used for encryption
    """
    log.debug("Creating Github repository secret.")
    encrypted_value = encrypt_sync_secret(public_key_value, token)
    # the parameters required by the Github API
    params = {"encrypted_value": encrypted_value, "key_id": public_key_id}
    # the authentification header
    headers = {"Authorization": f"token {token}"}
    # the url used for PUT
    put_url = f"https://api.github.com/repos/{username}/{repo_name}/actions/secrets/CT_SYNC_TOKEN"
    requests.put(put_url, headers=headers, data=json.dumps(params))


def encrypt_sync_secret(public_key: str, token: Union[str, bool]) -> str:
    """
    Encrypt the sync secret (which is the PAT).

    :param public_key: Public key of the repo we want to create a secret for
    :param token: The users PAT with repo scope as the secret
    :return: The encrypted secret (PAT)
    """
    """Encrypt a Unicode string using the public key."""
    log.debug("Encrypting Github repository secret.")
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(token.encode("utf-8"))  # type: ignore

    return b64encode(encrypted).decode("utf-8")


def decrypt_pat() -> str:
    """
    Decrypt the encrypted PAT.

    :return: The decrypted Personal Access Token for GitHub
    """
    log.debug(f"Decrypting personal access token using key saved in {ConfigCommand.KEY_PAT_FILE}.")
    # read key and encrypted PAT from files
    with open(ConfigCommand.KEY_PAT_FILE, "rb") as f:
        key = f.readline()
    fer = Fernet(key)
    log.debug(f"Reading personal access token from {ConfigCommand.CONF_FILE_PATH}.")
    encrypted_pat = load_yaml_file(ConfigCommand.CONF_FILE_PATH)["pat"]
    # decrypt the PAT and decode it to string
    console.print("[bold blue]Decrypting personal access token.")
    log.debug("Successfully decrypted personal access token.")
    decrypted_pat = fer.decrypt(encrypted_pat).decode("utf-8")

    return decrypted_pat


def load_github_username() -> str:
    """
    Load the username from cfg file.

    :return: The users Github account name
    """
    return load_yaml_file(ConfigCommand.CONF_FILE_PATH)["github_username"]


def handle_failed_github_repo_creation(e: Union[ConnectionError, GithubException]) -> None:
    """
    Called, when the automatic GitHub repo creation process failed during the create process. As this may have various issue sources,
    try to provide the user a detailed error message for the individual exception and inform them about what they should/can do next.

    :param e: The exception that has been thrown
    """
    # output the error dict thrown by PyGitHub due to an error related to GitHub
    if isinstance(e, GithubException):
        console.print(
            "[bold red]\nError while trying to create a Github repo due to an error related to Github API. "
            "See below output for detailed information!\n"
        )
        format_github_exception(e.data)
    # output an error that might occur due to a missing internet connection
    elif isinstance(e, ConnectionError):
        console.print(
            "[bold red]Error while trying to establish a connection to https://github.com. Do you have an active internet connection?"
        )


def format_github_exception(data: dict) -> None:
    """
    Format the github exception thrown by PyGitHub in a nice way and output it.

    :param data: The exceptions data as a dict
    """
    for section, description in data.items():
        if not isinstance(description, list):
            console.print(f"[bold red]{section.capitalize()}: {description}")
        else:
            console.print(f"[bold red]{section.upper()}: ")
            messages = [
                val if not isinstance(val, dict) and not isinstance(val, set) else github_exception_dict_repr(val)
                for val in description
            ]  # type: ignore
            console.print("[bold red]\n".join(msg for msg in messages))


def github_exception_dict_repr(messages: Union[Dict[Any, Any], Set[Any]]) -> str:
    """
    String representation for Github exception dict thrown by PyGitHub.

    :param messages: The messages as a dict
    """
    return "\n".join(f"{section.capitalize()}: {description}" for section, description in messages.items())  # type: ignore


def is_git_accessible() -> bool:
    """
    Verifies that git is accessible and in the PATH.

    :return: True if accessible, false if not
    """
    log.debug("Testing whether git is accessible.")
    git_installed = Popen(["git", "--version"], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    (git_installed_stdout, git_installed_stderr) = git_installed.communicate()
    if git_installed.returncode != 0:
        console.print("[bold red]Could not find 'git' in the PATH. Is it installed?")
        console.print("[bold red]Run command was: 'git --version '")
        log.debug("git is not accessible!")
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
        log.debug(f"Creating Github label {label[0]}")
        try:
            repo.create_label(name=label[0], color=label[1])
        except GithubException:
            log.debug(f"Unable to create label {label[0]}")
            console.print(f"[bold red]Unable to create label {label[0]} due to permissions")


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
