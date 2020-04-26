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
        '""reorder the list of commands when listing the help""'
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
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        sim_commands = most_similar_command(cmd_name, MAIN_COMMANDS)

        matches = [x for x in self.list_commands(ctx) if x in sim_commands]
        if not matches:
            ctx.fail(click.style('Unknown command and no similar command was found!', fg='red'))
        elif len(matches) == 1:
            click.echo(click.style(f'Unknown command! Will use best match {matches[0]}.', fg='red'))
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail(click.style('Unknown command. Most similar commands were %s' % ', '.join(sorted(matches)), fg='red'))
