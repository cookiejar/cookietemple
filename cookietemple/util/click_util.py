import click

from cookietemple.util.suggest_similar_commands import MAIN_COMMANDS
from cookietemple.info.levensthein_dist import most_similar_command


class CustomHelpOrder(click.Group):
    """
    Customise the order of subcommands for --help
    https://stackoverflow.com/a/47984810/713980
    """

    def __init__(self, *args, **kwargs):
        self.help_priorities = {}
        super(CustomHelpOrder, self).__init__(*args, **kwargs)

    def get_help(self, ctx):
        self.list_commands = self.list_commands_for_help
        return super(CustomHelpOrder, self).get_help(ctx)

    def list_commands_for_help(self, ctx):
        """reorder the list of commands when listing the help"""
        commands = super(CustomHelpOrder, self).list_commands(ctx)
        return (c[1] for c in sorted((self.help_priorities.get(command, 1000), command) for command in commands))

    def command(self, *args, **kwargs):
        """Behaves the same as `click.Group.command()` except capture
        a priority for listing command names in help.
        """
        help_priority = kwargs.pop('help_priority', 1000)
        help_priorities = self.help_priorities

        def decorator(f):
            cmd = super(CustomHelpOrder, self).command(*args, **kwargs)(f)
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
        sim_commands = most_similar_command(cmd_name, MAIN_COMMANDS)

        matches = [cmd for cmd in self.list_commands(ctx) if cmd in sim_commands]
        if not matches:
            ctx.fail(click.style('Unknown command and no similar command was found!', fg='red'))
        elif len(matches) == 1:
            click.echo(click.style(f'Unknown command! Will use best match ', fg='red') + click.style(f'{matches[0]}.', fg='green'))
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail(click.style(f'Unknown command. Most similar commands were {", ".join(sorted(matches))}', fg='red'))

    @staticmethod
    def args_not_provided(ctx, cmd: str) -> None:
        """
        Print a fail message depending on the command.
        :param ctx: Click app context
        :param cmd: The invoked subcommand
        """
        if cmd == 'info':
            ctx.fail('Failed to execute ' + click.style(f'{cmd.upper()}. ', fg='red') + 'Please provide a valid handle like \'cli\' as argument.')

        elif cmd == 'bump-version':
            ctx.fail('Failed to execute ' + click.style(f'{cmd.upper()}. ', fg='red') + 'Please specify a new version like \'1.2.3\' as first argument.')
