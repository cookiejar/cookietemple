import click
import os
import logging

from dataclasses import dataclass
from distutils.dir_util import copy_tree
from subprocess import Popen, PIPE
from github import Github


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
    github_username: str = click.prompt('Please enter your Github account username: ',
                                        type=str)
    github_password: str = click.prompt('Please enter your Github account password: ',
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
    authenticated_github_user = Github(github_username, github_password)
    user = authenticated_github_user.get_user()

    # Create new repository
    click.echo(click.style('Creating Github repository.', fg='blue'))
    if is_github_org:
        org = authenticated_github_user.get_organization(github_org)
        org.create_repo(project_name, description=project_description, private=private)
    else:
        user.create_repo(project_name, description=project_description, private=private)

    conducted_subprocesses = []
    repository = f'{os.getcwd()}/{project_name}'  # TODO note that we are using the current working directory to clone to path
                              #  if we ever add a 'output' parameter to COOKIETEMPLE create we also have change this here

    # TODO ORG SUPPORT NOT WORKING
    # TODO We need to replace the username with the organization every time here, since it will be created at organization/project_name

    # git clone
    click.echo(click.style('Cloning empty Github repoitory.', fg='blue'))
    git_clone = Popen(['git', 'clone', fr'https://{github_username}:{github_password}@github.com/{github_username}/{project_name}', repository],
                      stdout=PIPE, stderr=PIPE, universal_newlines=True)
    (git_clone_stdout, git_clone_stderr) = git_clone.communicate()
    conducted_subprocesses.append(ConductedSubprocess(git_clone,
                                                      'git clone',
                                                      rf'git clone https://{github_username}:github_password@github.com/{github_username}/{project_name}',
                                                      git_clone_stdout,
                                                      git_clone_stderr))

    # Copy files which should be included in the initial commit -> basically the template
    copy_tree(template_creation_path, repository)

    # git add
    click.echo(click.style('Staging template.', fg='blue'))
    git_add = Popen(['git', 'add', '.'],
                    cwd=repository, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    (git_add_stdout, git_add_stderr) = git_add.communicate()
    conducted_subprocesses.append(ConductedSubprocess(git_add,
                                                      'git add',
                                                      r'git add .',
                                                      git_add_stdout,
                                                      git_add_stderr))

    # git commit
    git_commit = Popen(['git', 'commit', '-m', r'"Initial COOKIETEMPLE commit"'],  # Replace with name and version of the template here
                       cwd=repository, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    (git_commit_stdout, git_commit_stderr) = git_commit.communicate()
    conducted_subprocesses.append(ConductedSubprocess(git_commit,
                                                      'git commit',
                                                      r'git commit -m "Initial COOKIETEMPLE commit"',
                                                      git_commit_stdout,
                                                      git_commit_stderr))

    # git push to origin master and set as default
    click.echo(click.style('Pushing template to Github origin master.', fg='blue'))
    git_push_master = Popen(['git', 'push', '-u', f'https://{github_username}:{github_password}@github.com/{github_username}/{project_name}', '--all'],
                     cwd=repository, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    (git_push_master_stdout, git_push_master_stderr) = git_push_master.communicate()
    conducted_subprocesses.append(ConductedSubprocess(git_push_master,
                                                      'git push origin master',
                                                      rf'git push -u https://{github_username}:github_password@github.com/{github_username}/{project_name} --all',
                                                      git_push_master_stdout,
                                                      git_push_master_stderr))

    # git create development branch
    click.echo(click.style('Creating development branch.', fg='blue'))
    git_checkout_b_development = Popen(['git', 'checkout', '-b', 'development'],
                     cwd=repository, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    (git_checkout_b_development_stdout, git_checkout_b_development_stderr) = git_checkout_b_development.communicate()
    conducted_subprocesses.append(ConductedSubprocess(git_checkout_b_development,
                                                      'git checkout -b development',
                                                      rf'git checkout -b development',
                                                      git_checkout_b_development_stdout,
                                                      git_checkout_b_development_stderr))

    # git push to origin development
    click.echo(click.style('Pushing template to Github origin development.', fg='blue'))
    git_push_development = Popen(['git', 'push', f'https://{github_username}:{github_password}@github.com/{github_username}/{project_name}'],
                     cwd=repository, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    (git_push_development_stdout, git_push_development_stderr) = git_push_development.communicate()
    conducted_subprocesses.append(ConductedSubprocess(git_push_development,
                                                      'git push origin development',
                                                      rf'git push https://{github_username}:github_password@github.com/{github_username}/{project_name}',
                                                      git_push_development_stdout,
                                                      git_push_development_stderr))

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
            logging.warning(f'Subprocess {conducted_subprocess.name} ran with errors!')
            click.echo(click.style(f'Subprocess {conducted_subprocess.name} ran with errors!', fg='red'))
            click.echo(click.style(f'Run command was: {conducted_subprocess.run_command}', fg='red'))
            click.echo(click.style(f'Error was: {conducted_subprocess.stderr}', fg='red'))

# TODO Check if git is installed and raise an error if not
# TODO CHeck if git user.name and user.email are set properly
# Reference: https://github.com/pyscaffold/pyscaffold/blob/master/src/pyscaffold/info.py
