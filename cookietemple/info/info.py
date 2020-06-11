import os
import sys
import click
from rich.style import Style
from rich.console import Console
from rich.table import Table
from rich.box import HEAVY_HEAD
from cookietemple.custom_cookietemple_cli.levensthein_dist import most_similar_command
from cookietemple.util.yaml_util import load_yaml_file
from cookietemple.util.dict_util import is_nested_dictionary
from cookietemple.custom_cookietemple_cli.suggest_similar_commands import load_available_handles


class TemplateInfo:
    """
    Present info in a nice layout about specific subsets of templates
    """

    def __init__(self):
        self.WD = os.path.dirname(__file__)
        self.TEMPLATES_PATH = f'{self.WD}/../create/templates'

    def show_info(self, handle: str) -> None:
        """
        Displays detailed information of a domain/language/template

        :param handle: domain/language/template handle (examples: cli or cli-python)
        """
        # list of all templates that should be printed according to the passed handle
        templates_to_print = []
        available_templates = load_yaml_file(f'{self.TEMPLATES_PATH}/available_templates.yml')

        specifiers = handle.split('-')
        domain = specifiers[0]
        global template_info

        # only domain specified
        if len(specifiers) == 1:
            try:
                template_info = available_templates[domain]
            except KeyError:
                self.handle_non_existing_command(handle)
        # domain, subdomain, language
        elif len(specifiers) > 2:
            try:
                sub_domain = specifiers[1]
                language = specifiers[2]
                template_info = available_templates[domain][sub_domain][language]
            except KeyError:
                self.handle_non_existing_command(handle)
        # domain, language OR domain, subdomain
        else:
            try:
                second_specifier = specifiers[1]
                template_info = available_templates[domain][second_specifier]
            except KeyError:
                self.handle_non_existing_command(handle)

        # Add all templates under template_info to list
        self.flatten_nested_dict(template_info, templates_to_print)

        for template in templates_to_print:
            template[2] = TemplateInfo.set_linebreaks(template[2])

        table = Table(title=f'[bold]Info on COOKIETEMPLE´s {handle} templates', title_style="blue", header_style=Style(color="blue", bold=True), box=HEAVY_HEAD)

        table.add_column("Name", justify="left", style="green", no_wrap=True)
        table.add_column("Handle", justify="left")
        table.add_column("Long Description", justify="left")
        table.add_column("Available Libraries", justify="left")
        table.add_column("Version", justify="left")

        for template in templates_to_print:
            table.add_row(f'[bold]{template[0]}', template[1], template[2], template[3], template[4])

        console = Console()
        console.print(table)

    def flatten_nested_dict(self, template_info_, templates_to_print) -> None:
        """
        Flatten an arbitrarily deep nested dict and creates a list of list containing all available
        templates for the specified doamin/subdomain and/or language.

        :param template_info_: The dict containing the yaml parsed info for all available templates the user wants to gather some information
        :param templates_to_print: A list of templates string representations, that will be printed to console
        """
        if is_nested_dictionary(template_info_):
            for templ in template_info_.values():
                if not is_nested_dictionary(templ):
                    templates_to_print.append([templ['name'], templ['handle'], templ['long description'],
                                               templ['available libraries'], templ['version']])
                else:
                    self.flatten_nested_dict(templ, templates_to_print)
        else:
            # a single template to append was reached
            templates_to_print.append([template_info_['name'], template_info_['handle'], template_info_['long description'],
                                       template_info_['available libraries'], template_info_['version']])

    @staticmethod
    def set_linebreaks(desc: str) -> str:
        """
        Sets newlines after max 45 characters (or the latest space to avoid non-sense separation)

        :param desc: The parsed long description for the sepcific template
        :return: The formatted string with inserted newlines
        """
        linebreak_limit = 50
        last_space = -1
        cnt = 0
        idx = 0

        while idx < len(desc):
            if cnt == linebreak_limit:
                # set a line break at the last space encountered to avoid separating words
                desc = desc[:last_space] + '\n' + desc[last_space + 1:]
                cnt = 0
            elif desc[idx] == ' ':
                last_space = idx
            cnt += 1
            idx += 1

        return desc

    @staticmethod
    def non_existing_handle() -> None:
        """
        Handling key not found access error for non existing template handles.
        Displays an error message and terminates cookietemple.
        """
        click.echo(click.style('Handle does not exist. Please enter a valid handle.\nUse ', fg='red')
                   + click.style('cookietemple list', fg='blue')
                   + click.style(' to display all template handles.', fg='red'))
        sys.exit(0)

    def handle_non_existing_command(self, handle: str) -> None:
        """
        Handle the case, when an unknown handle was entered and try to find a similar handle.
        :param handle: The non existing handle
        """
        available_handles = load_available_handles()
        most_sim, action = most_similar_command(handle, available_handles)
        if most_sim:
            # found exactly one similar handle
            if len(most_sim) == 1 and action == 'use':
                click.echo(click.style(f'Unknown handle \'{handle}\'. See ', fg='red') + click.style('cookietemple list ', fg='blue') +
                           click.style('for all valid handles.\n', fg='red'))
                click.echo(click.style('Will use best match ', fg='red') + click.style(f'{most_sim[0]}.\n', fg='green'))
                # use best match if exactly one similar handle was found
                self.show_info(most_sim[0])
            elif len(most_sim) == 1 and action == 'suggest':
                click.echo(click.style(f'Unknown handle \'{handle}\'. See ', fg='red') + click.style('cookietemple list ', fg='blue') +
                           click.style('for all valid handles.\n', fg='red'))
                click.echo(click.style('Did you mean ', fg='red') + click.style(f'{most_sim[0]}?\n', fg='green'))
            else:
                # found multiple similar handles
                nl = '\n'
                click.echo(click.style(f'Unknown handle \'{handle}\'. See ', fg='red') + click.style('cookietemple list ', fg='green') +
                           click.style('for all valid handles.\nMost similar handles are:', fg='red') + click.style(f'{nl}{nl.join(sorted(most_sim))}',
                                                                                                                    fg='green'))
            sys.exit(0)

        else:
            # found no similar handles
            TemplateInfo.non_existing_handle()
