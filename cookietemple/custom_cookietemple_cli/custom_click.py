import click
import sys
from pathlib import Path
from configparser import NoSectionError

from cookietemple.custom_cookietemple_cli.suggest_similar_commands import MAIN_COMMANDS
from cookietemple.custom_cookietemple_cli.levensthein_dist import most_similar_command
from cookietemple.bump_version.bump_version import VersionBumper


class HelpErrorHandling(click.Group):
    """
    Customise the order of subcommands for --help
    https://stackoverflow.com/a/47984810/713980
    """

    def __init__(self, *args, **kwargs):
        self.help_priorities = {}
        super(HelpErrorHandling, self).__init__(*args, **kwargs)

    def get_help(self, ctx):
        self.list_commands = self.list_commands_for_help
        return super(HelpErrorHandling, self).get_help(ctx)

    def list_commands_for_help(self, ctx):
        """reorder the list of commands when listing the help"""
        commands = super(HelpErrorHandling, self).list_commands(ctx)
        return (c[1] for c in sorted((self.help_priorities.get(command, 1000), command) for command in commands))

    def command(self, *args, **kwargs):
        """Behaves the same as `click.Group.command()` except capture
        a priority for listing command names in help.
        """
        help_priority = kwargs.pop('help_priority', 1000)
        help_priorities = self.help_priorities

        def decorator(f):
            cmd = super(HelpErrorHandling, self).command(*args, **kwargs)(f)
            help_priorities[cmd.name] = help_priority
            return cmd

        return decorator

    def get_command(self, ctx, cmd_name):
        """
        Override the get_command of Click.
        If an unknown command is given, try to determine a similar command.
        If no similar command could´ve been found, exit with an error message.
        Else use the most similar command while printing a status message for the user.

        :param ctx: The given Click context for the group
        :param cmd_name: The command invoked with Click
        """
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        sim_commands, action = most_similar_command(cmd_name, MAIN_COMMANDS)

        matches = [cmd for cmd in self.list_commands(ctx) if cmd in sim_commands]

        # no similar commands could be found
        if not matches:
            ctx.fail(click.style('Unknown command and no similar command was found!', fg='red'))
        elif len(matches) == 1 and action == 'use':
            click.echo(click.style('Unknown command! Will use best match ', fg='red') + click.style(f'{matches[0]}.', fg='green'))
            return click.Group.get_command(self, ctx, matches[0])
        elif len(matches) == 1 and action == 'suggest':
            ctx.fail(click.style('Unknown command! Did you mean ', fg='red') + click.style(f'{matches[0]}?', fg='green'))

        # a few similar commands were found, print a info message
        ctx.fail(click.style('Unknown command. Most similar commands were', fg='red') + click.style(f'{", ".join(sorted(matches))}', fg='red'))

    @staticmethod
    def args_not_provided(ctx, cmd: str) -> None:
        """
        Print a fail message depending on the command.
        :param ctx: Click app context
        :param cmd: The invoked subcommand
        """
        if cmd == 'info':
            click.echo(click.style('Failed to execute ', fg='red') + click.style(f'{cmd.upper()}. ', fg='red')
                       + click.style('Please provide a valid handle like ', fg='blue')
                       + click.style('cli ', fg='green') + click.style('as argument', fg='blue'))
            sys.exit(1)

        elif cmd == 'bump-version':
            click.echo(click.style('Failed to execute ', fg='red') + click.style(f'{cmd.upper()}. ', fg='red')
                       + click.style('Please provide a new version like ', fg='blue')
                       + click.style('1.2.3 ', fg='green') + click.style('as first argument', fg='blue'))
            sys.exit(1)

        elif cmd == 'config':
            click.echo(click.style('Failed to execute ', fg='red') + click.style(f'{cmd.upper()}. ', fg='red')
                       + click.style('Please provide a valid argument. You can choose general, github or all.', fg='blue'))
            sys.exit(1)


def print_project_version(ctx, param, value) -> None:
    """
    Print the current project version.
    """
    # if context uses resilient parsing (no changes of execution flow) or no flag value is provided, do nothing
    if not value or ctx.resilient_parsing:
        return
    try:
        click.echo(click.style('Current project version is ', fg='blue') + click.style(VersionBumper(Path.cwd()).CURRENT_VERSION, fg='green'))
        ctx.exit()
    # currently, its only possible to get project version from top level project dir where the cookietemple.cfg file is
    except NoSectionError:
        ctx.fail(click.style('Unable to read from cookietemple.cfg file.\nMake sure your current working directory has a cookietemple.cfg file '
                             'when running bump-version with the --project-version flag!', fg='red'))
