import click
import os
import logging

from dataclasses import dataclass
from distutils.dir_util import copy_tree
from subprocess import Popen, PIPE
from github import Github, GithubException
from git import Repo


@dataclass
class ConductedSubprocess:
    subprocess: Popen
    name: str
    run_command: str
    stdout: str
    stderr: str


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

    access_token: str = click.prompt('Please enter your GitHub acess token: ',
                                     type=str,
                                     hide_input=True)

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

    create_dependabot_label(repo=repo, name="Dependabot")

    conducted_subprocesses = []
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
    verify_git_subprocesses(conducted_subprocesses)
    click.echo(click.style(f'Successfully created a Github repository at https://github.com/{github_username}/{project_name}', fg='green'))


def verify_git_subprocesses(conducted_subprocesses: list) -> None:
    """
    Verifies that all subprocesses during Github repository creation ran without errors.
    Logs any occuring errors.

    :param conducted_subprocesses: List of all git subprocesses that were run when creating and pushing to the repository
    """
    click.echo(click.style('Verifying git subprocesses.', fg='blue'))
    for conducted_subprocess in conducted_subprocesses:
        if conducted_subprocess.subprocess.returncode != 0:
            logging.error(f'Subprocess {conducted_subprocess.name} ran with errors!')
            click.echo(click.style(f'Subprocess {conducted_subprocess.name} ran with errors!', fg='red'))
            click.echo(click.style(f'Run command was: {conducted_subprocess.run_command}', fg='red'))
            click.echo(click.style(f'Error was: {conducted_subprocess.stderr}', fg='red'))


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


def create_dependabot_label(repo, name):
    try:
        repo.create_label(name=name, color="1BB0CE")
    except GithubException:
        click.echo(click.style("Unable to create label {} due to permissions".format(name), fg='red'))
