import collections
import io
from rich.console import Console
import click
import sys
from pathlib import Path
from configparser import NoSectionError

from cookietemple.custom_cli.suggest_similar_commands import MAIN_COMMANDS
from cookietemple.custom_cli.levensthein_dist import most_similar_command
from cookietemple.bump_version.bump_version import VersionBumper


class HelpErrorHandling(click.Group):
    """
    Customise the help command
    """
    def __init__(self, name=None, commands=None, **kwargs):
        super(HelpErrorHandling, self).__init__(name, commands, **kwargs)
        self.commands = commands or collections.OrderedDict()

    def list_commands(self, ctx):
        return self.commands

    def main_options(self, ctx, formatter) -> None:
        """
        Load the main options and display them in a customized option section.
        :param ctx: clicks context
        :param formatter: the formatter for output
        """
        ct_main_options = []
        for p in ctx.command.params:
            ct_main_options.append(('--' + p.name + ': ', p.help))
        ct_main_options.append(('--help: ', 'Get detailed info on a command.'))
        with formatter.section(self.get_rich_value('Options')):
            for t in ct_main_options:
                formatter.write_text(f'{t[0] + t[1]}')

    def format_help(self, ctx, formatter):
        """
        Call format_help function with cookietemples customized functions.
        """
        self.format_usage(ctx, formatter)
        self.format_options(ctx, formatter)
        self.format_commands(ctx, formatter)

    def format_usage(self, ctx, formatter):
        """
        Overwrite format_usage method of class MultiCommand for customized usage section output.
        """
        formatter.write_text(f'{self.get_rich_value("Usage:")} {" ".join(super().collect_usage_pieces(ctx))}')

    def format_options(self, ctx, formatter):
        """
        Overwrite the format_options method of class MultiCommand for customized option output.
        This is internally called by format_help() which itself is called by get_help().
        """
        self.main_options(ctx, formatter)

    def format_commands(self, ctx, formatter):
        """
        Overwrite the format_commands method of class MultiCommand for customized commands output.
        """
        formatter.width = 120
        formatter.write_paragraph()

        with formatter.section(self.get_rich_value("General Commands")):
            formatter.write_text(
                f"{self.commands.get('list').name}\t\t{self.commands.get('list').get_short_help_str(limit=150)}")
            formatter.write_text(
                f"{self.commands.get('info').name}\t\t{self.commands.get('info').get_short_help_str(limit=150)}")
            formatter.write_text(
                f"{self.commands.get('config').name}\t\t{self.commands.get('config').get_short_help_str(limit=150)}")
            formatter.write_text(
                f"{self.commands.get('upgrade').name}\t\t{self.commands.get('upgrade').get_short_help_str(limit=150)}")

        with formatter.section(self.get_rich_value("Commands for cookietemple project")):
            formatter.write_text(
                f"{self.commands.get('create').name}\t\t{self.commands.get('create').get_short_help_str(limit=150)}")
            formatter.write_text(
                f"{self.commands.get('lint').name}\t\t{self.commands.get('lint').get_short_help_str(limit=150)}")
            formatter.write_text(
                f"{self.commands.get('bump-version').name}\t{self.commands.get('bump-version').get_short_help_str(limit=150)}")
            formatter.write_text(
                f"{self.commands.get('sync').name}\t\t{self.commands.get('sync').get_short_help_str(limit=150)}")

        with formatter.section(self.get_rich_value("Special commands")):
            formatter.write_text(
                f"{self.commands.get('warp').name}\t\t{self.commands.get('warp').get_short_help_str(limit=150)}")

        with formatter.section(self.get_rich_value("Examples")):
            formatter.write_text("$ cookietemple create")
            formatter.write_text("$ cookietemple bump-version 1.0.0 .")
            formatter.write_text("$ cookietemple config all")
            formatter.write_text("$ cookietemple info python")

        with formatter.section(self.get_rich_value("Learn more")):
            formatter.write_text("Use cookietemple <command> --help for more information about a command. You may also want to take a look at our docs at "
                                 "https://cookietemple.readthedocs.io/ .")

        with formatter.section(self.get_rich_value("Feedback")):
            formatter.write_text("We are always curious about your opinion on cookietemple. Join our Discord at "
                                 "https://discord.com/channels/708008788505919599/708008788505919602 and drop us message: cookies await you.")

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
                       + click.style('Please provide a valid argument. You can choose general, pat or all.', fg='blue'))
            sys.exit(1)

    def get_rich_value(self, output: str, is_header=True) -> str:
        """
        Return a string which contains the output to console rendered by rich for the click formatter.
        :param output: the output string, that should be rendered by rich
        :param is_header: is output a header section?
        """
        sio = io.StringIO()
        console = Console(file=sio, force_terminal=True)
        if is_header:
            console.print(f"[bold #1874cd]{output}")

        return sio.getvalue().replace('\n', '')


def print_project_version(ctx, param, value) -> None:
    """
    Print the current project version.
    """
    # if context uses resilient parsing (no changes of execution flow) or no flag value is provided, do nothing
    if not value or ctx.resilient_parsing:
        return
    try:
        click.echo(click.style('Current project version is ', fg='blue') + click.style(VersionBumper(Path.cwd(), False).CURRENT_VERSION, fg='green'))
        ctx.exit()
    # currently, its only possible to get project version from top level project dir where the cookietemple.cfg file is
    except NoSectionError:
        ctx.fail(click.style('Unable to read from cookietemple.cfg file.\nMake sure your current working directory has a cookietemple.cfg file '
                             'when running bump-version with the --project-version flag!', fg='red'))
