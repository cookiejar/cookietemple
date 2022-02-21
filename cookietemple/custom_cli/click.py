import collections
import io
import sys
from configparser import NoSectionError
from pathlib import Path

import click
from rich import print
from rich.console import Console

import cookietemple
from cookietemple.bump_version.bump_version import VersionBumper
from cookietemple.common.levensthein_dist import most_similar_command
from cookietemple.common.suggest_similar_commands import MAIN_COMMANDS


class HelpErrorHandling(click.Group):
    """
    Customise the help command
    """

    def __init__(self, name=None, commands=None, **kwargs):
        super().__init__(name, commands, **kwargs)
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
        # NOTE: this only works for options as arguments do not have a help attribute per default
        for p in ctx.command.params:
            ct_main_options.append(("--" + p.name + ": ", p.help))
        ct_main_options.append(("--help: ", "   Get detailed info on a command."))
        with formatter.section(HelpErrorHandling.get_rich_value("Options")):
            for t in ct_main_options:
                formatter.write_text(f"{t[0] + t[1]}")

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
        formatter.write_text(
            f'{HelpErrorHandling.get_rich_value("Usage:")} cookietemple {" ".join(super().collect_usage_pieces(ctx))}'
        )

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

        with formatter.section(HelpErrorHandling.get_rich_value("General Commands")):
            formatter.write_text(
                f"{self.commands.get('list').name}\t\t{self.commands.get('list').get_short_help_str(limit=150)}"
            )
            formatter.write_text(
                f"{self.commands.get('info').name}\t\t{self.commands.get('info').get_short_help_str(limit=150)}"
            )
            formatter.write_text(
                f"{self.commands.get('config').name}\t\t{self.commands.get('config').get_short_help_str(limit=150)}"
            )
            formatter.write_text(
                f"{self.commands.get('upgrade').name}\t\t{self.commands.get('upgrade').get_short_help_str(limit=150)}"
            )

        with formatter.section(HelpErrorHandling.get_rich_value("Commands for cookietemple project")):
            formatter.write_text(
                f"{self.commands.get('create').name}\t\t{self.commands.get('create').get_short_help_str(limit=150)}"
            )
            formatter.write_text(
                f"{self.commands.get('lint').name}\t\t{self.commands.get('lint').get_short_help_str(limit=150)}"
            )
            formatter.write_text(
                f"{self.commands.get('bump-version').name}\t{self.commands.get('bump-version').get_short_help_str(limit=150)}"
            )
            formatter.write_text(
                f"{self.commands.get('sync').name}\t\t{self.commands.get('sync').get_short_help_str(limit=150)}"
            )

        with formatter.section(HelpErrorHandling.get_rich_value("Special commands")):
            formatter.write_text(
                f"{self.commands.get('warp').name}\t\t{self.commands.get('warp').get_short_help_str(limit=150)}"
            )

        with formatter.section(HelpErrorHandling.get_rich_value("Examples")):
            formatter.write_text("$ cookietemple create")
            formatter.write_text("$ cookietemple bump-version 1.0.0 .")
            formatter.write_text("$ cookietemple config all")
            formatter.write_text("$ cookietemple info python")

        with formatter.section(HelpErrorHandling.get_rich_value("Learn more")):
            formatter.write_text(
                "Use cookietemple <command> --help for more information about a command. You may also want to take a look at our docs at "
                "https://cookietemple.readthedocs.io/."
            )

        with formatter.section(HelpErrorHandling.get_rich_value("Feedback")):
            formatter.write_text(
                "We are always curious about your opinion on cookietemple. Join our Discord at "
                "https://discord.gg/CwRXMdSg and drop us a message: cookies await you."
            )

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
            ctx.fail(click.style("Unknown command and no similar command was found!", fg="red"))
        elif len(matches) == 1 and action == "use":
            print(f"[bold red]Unknown command! Will use best match [green]{matches[0]}")
            return click.Group.get_command(self, ctx, matches[0])
        elif len(matches) == 1 and action == "suggest":
            ctx.fail(
                click.style("Unknown command! Did you mean ", fg="red") + click.style(f"{matches[0]}?", fg="green")
            )

        # a few similar commands were found, print a info message
        ctx.fail(
            click.style("Unknown command. Most similar commands were", fg="red")
            + click.style(f'{", ".join(sorted(matches))}', fg="red")
        )

    @staticmethod
    def args_not_provided(ctx, cmd: str) -> None:
        """
        Print a fail message depending on the command.
        :param ctx: Click app context
        :param cmd: The invoked subcommand
        """
        if cmd == "info":
            print(
                f"[bold red]Failed to execute [bold green]{cmd}.\n[bold blue]Please provide a valid handle like [bold green]cli "
                "[bold blue]as argument."
            )
            sys.exit(1)

        elif cmd == "config":
            print(
                f"[bold red]Failed to execute [bold green]{cmd}.\n[bold blue]Please provide a valid argument. You can choose general, pat or all."
            )
            sys.exit(1)

    @staticmethod
    def get_rich_value(output: str, is_header=True) -> str:
        """
        Return a string which contains the output to console rendered by rich for the click formatter.
        :param output: the output string, that should be rendered by rich
        :param is_header: is output a header section?
        """
        sio = io.StringIO()
        console = Console(file=sio, force_terminal=True)
        if is_header:
            console.print(f"[bold #1874cd]{output}")

        return sio.getvalue().replace("\n", "")


class CustomHelpSubcommand(click.Command):
    """
    Customize the help output for each subcommand
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def format_help(self, ctx, formatter):
        """
        Custom implementation of formatting help for each subcommand.
        Use the overwritten format functions this class provides to output help for each subcommand cookietemple provides.
        """
        formatter.width = 120
        self.format_usage(ctx, formatter)
        self.format_help_text(ctx, formatter)
        self.format_options(ctx, formatter)

    def format_usage(self, ctx, formatter):
        """
        Custom implementation if formatting the usage of each subcommand.
        Usage section with a styled header will be printed.
        """
        formatter.write_text(
            f'{HelpErrorHandling.get_rich_value("Usage: ")}cookietemple {self.name} {" ".join(self.collect_usage_pieces(ctx))}'
        )

    def format_help_text(self, ctx, formatter):
        """
        Custom implementation of formatting the help text of each subcommand.
        The help text will be printed as normal. A separate arguments section will be added below with all arguments and a short help message
        for each of them and a styled header in order to keep things separated.
        """
        formatter.write_paragraph()
        formatter.write_text(self.help)
        args = [("--" + param.name, param.helpmsg) for param in self.params if type(param) == CustomArg]
        if args:
            with formatter.section(HelpErrorHandling.get_rich_value("Arguments")):
                formatter.write_dl(args)

    def format_options(self, ctx, formatter):
        """
        Custom implementation of formatting the options of each subcommand.
        The options will be displayed in their relative order with their corresponding help message and a styled header.
        """
        options = [
            ("--" + param.name.replace("_", "-"), param.help)
            for param in self.params
            if type(param) == click.core.Option
        ]
        help_option = self.get_help_option(ctx)
        options.append(("--" + help_option.name, help_option.help))
        with formatter.section(HelpErrorHandling.get_rich_value("Options")):
            formatter.write_dl(options)

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

        return sio.getvalue().replace("\n", "")


class CustomArg(click.Argument):
    """
    A custom argument implementation of click.Argument class in order to provide a short helpmessage for each argument of a command.
    """

    def __init__(self, *args, **kwargs):
        self.helpmsg = kwargs.pop("helpmsg")
        super().__init__(*args, **kwargs)


def print_project_version(ctx, param, value) -> None:
    """
    Print the current project version.
    """
    # if context uses resilient parsing (no changes of execution flow) or no flag value is provided, do nothing
    if not value or ctx.resilient_parsing:
        return
    try:
        print(f"[bold blue]Current project version is [bold green]{VersionBumper(Path.cwd(), False).CURRENT_VERSION}!")
        ctx.exit()
    # currently, its only possible to get project version from top level project dir where the cookietemple.cfg file is
    except NoSectionError:
        ctx.fail(
            click.style(
                "Unable to read from cookietemple.cfg file.\nMake sure your current working directory has a cookietemple.cfg file "
                "when running bump-version with the --project-version flag!",
                fg="red",
            )
        )


def print_cookietemple_version(ctx, param, value):
    """
    Print cookietemple version styled with rich.
    """
    # if context uses resilient parsing (no changes of execution flow) or no flag value is provided, do nothing
    if not value or ctx.resilient_parsing:
        return
    try:
        print(f"[bold blue]Cookietemple version: {cookietemple.__version__}")
        ctx.exit()
    except click.ClickException:
        ctx.fail("An error occurred fetching cookietemples version!")
