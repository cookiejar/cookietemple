import logging
import os
import sys
from typing import List

from rich import print
from rich.box import HEAVY_HEAD
from rich.console import Console
from rich.style import Style
from rich.table import Table

from cookietemple.common.levensthein_dist import most_similar_command
from cookietemple.common.load_yaml import load_yaml_file
from cookietemple.common.suggest_similar_commands import load_available_handles
from cookietemple.util.dict_util import is_nested_dictionary

log = logging.getLogger(__name__)


class TemplateInfo:
    """
    Present info in a nice layout about specific subsets of templates
    """

    def __init__(self):
        self.WD = os.path.dirname(__file__)
        self.TEMPLATES_PATH = f"{self.WD}/../create/templates"
        self.available_handles = ""
        self.most_sim = []
        self.action = ""

    def show_info(self, handle: str) -> None:
        """
        Displays detailed information of a domain/language/template

        :param handle: domain/language/template handle (examples: cli or cli-python)
        """
        # list of all templates that should be printed according to the passed handle
        templates_to_print: List[str] = []
        available_templates = load_yaml_file(f"{self.TEMPLATES_PATH}/available_templates.yml")
        specifiers = handle.split("-")
        domain = specifiers[0]
        template_info: List[str] = []

        # only domain OR language specified
        if len(specifiers) == 1:
            log.debug("Only domain or language was specified.")
            try:
                template_info = available_templates[domain]
            except KeyError:
                self.handle_domain_or_language_only(handle, available_templates)
        # domain, subdomain, language
        elif len(specifiers) > 2:
            log.debug("A domain, subdomain and language was specified.")
            try:
                sub_domain = specifiers[1]
                language = specifiers[2]
                template_info = available_templates[domain][sub_domain][language]
            except KeyError:
                self.handle_non_existing_command(handle, True)
        # domain, language OR domain, subdomain
        else:
            log.debug("A domain and language OR domain and a subdomain was specified.")
            try:
                second_specifier = specifiers[1]
                template_info = available_templates[domain][second_specifier]
            except KeyError:
                self.handle_non_existing_command(handle, True)

        # Add all templates under template_info to list and output them
        self.flatten_nested_dict(template_info, templates_to_print)
        TemplateInfo.output_table(templates_to_print, handle)

    def handle_domain_or_language_only(self, handle: str, available_templates: dict) -> None:
        """
        Try to find a similar domain or treat handle as possible language
        :param handle: The handle inputted by the user
        :param available_templates: All available templates load from yml file as dict
        """
        # try to find a similar domain
        self.handle_non_existing_command(handle)
        # we found a similar handle matching a domain, use it (suggest it maybe later)
        if self.most_sim and self.action not in ("suggest", ""):
            self.print_console_output(handle)

        # input may be a language so try this
        templates_flatted: List[str] = []
        self.flatten_nested_dict(available_templates, templates_flatted)
        # load all available languages
        available_languages = TemplateInfo.load_available_languages(templates_flatted)
        # if handle exists as language in cookietemple output its available templates and exit with zero status
        if handle in available_languages:
            templates_to_print_ = [template for template in templates_flatted if handle in template[1]]
            TemplateInfo.output_table(templates_to_print_, handle)

        # the handle does not match any domain/language; is there a similar language?
        else:
            # save domain values for later use
            domain_handle, domain_action = self.most_sim, self.action
            # try to find a similar language for instant use
            self.most_sim, self.action = most_similar_command(handle, available_languages)
            # use language if available
            if self.most_sim and self.action not in ("", "suggest"):
                self.print_console_output(handle)
            # try to suggest a similar domain handle
            elif domain_action == "suggest" and domain_handle:
                TemplateInfo.print_suggestion(handle, domain_handle)
            # try to suggest a similar language handle
            elif self.action == "suggest" and self.most_sim:
                TemplateInfo.print_suggestion(handle, self.most_sim)
            # we're done there is no similar handle
            else:
                TemplateInfo.non_existing_handle()
        sys.exit(0)

    @staticmethod
    def output_table(templates_to_print: list, handle: str) -> None:
        """
        Output a nice looking, rich rendered table.
        :param templates_to_print: The templates tht should go into the table
        :param handle: The handle the user inputted
        """
        for template in templates_to_print:
            template[2] = TemplateInfo.set_linebreaks(template[2])

        log.debug("Building info table.")
        table = Table(
            title=f"[bold]Info on cookietemple´s {handle}",
            title_style="blue",
            header_style=Style(color="blue", bold=True),
            box=HEAVY_HEAD,
        )

        table.add_column("Name", justify="left", style="green", no_wrap=True)
        table.add_column("Handle", justify="left")
        table.add_column("Long Description", justify="left")
        table.add_column("Available Libraries", justify="left")
        table.add_column("Version", justify="left")

        for template in templates_to_print:
            table.add_row(f"[bold]{template[0]}", template[1], f"{template[2]}\n", template[3], template[4])

        log.debug("Printing info table.")
        console = Console()
        console.print(table)

    def handle_non_existing_command(self, handle: str, run_f: bool = False) -> None:
        """
        Handle the case, when an unknown handle was entered and try to find a similar handle.
        :param handle: The non existing handle
        :param run_f: Flag that indicates whether to run print to output or not (do not run in case of languages)
        """
        self.available_handles = load_available_handles()
        self.most_sim, self.action = most_similar_command(handle, self.available_handles)
        if run_f:
            self.print_console_output(handle)

    def print_console_output(self, handle) -> None:
        """
        Print similar command output to console.
        :param handle: The handle inputted by the user
        """
        if self.most_sim:
            # found exactly one similar handle
            if len(self.most_sim) == 1 and self.action == "use":
                print(f"[bold red]Unknown handle '{handle}'. See [green]cookietemple list [red]for all valid handles")
                print(f"[bold blue]Will use best match [green]{self.most_sim[0]}.\n")
                # use best match if exactly one similar handle was found
                self.show_info(self.most_sim[0])
            elif len(self.most_sim) == 1 and self.action == "suggest":
                self.print_suggestion(handle, self.most_sim)
            else:
                # found multiple similar handles
                nl = "\n"
                print(
                    f"[bold red]Unknown handle '{handle}'. See [green]cookietemple list [red]for all valid handles."
                    + f"\nMost similar handles are: [green]{nl}{nl.join(sorted(self.most_sim))}"
                )
            sys.exit(0)

        else:
            # found no similar handles
            TemplateInfo.non_existing_handle()

    @staticmethod
    def print_suggestion(handle: str, domain_handle: list) -> None:
        """
        Output a similar command suggestion message for the user
        :param handle: Handle inputted by the user
        :param domain_handle: A list of similar commands (will contain only one element most of the time)
        """
        print(f"[bold red]Unknown handle '{handle}'. See [green]cookietemple list [red] for all valid handles.\n")
        print(f"[bold red] Did you mean [green]{domain_handle[0]}?\n")

    @staticmethod
    def non_existing_handle() -> None:
        """
        Handling key not found access error for non existing template handles.
        Displays an error message and terminates cookietemple.
        """
        print(
            "[bold red]Handle does not exist. Please enter a valid handle.\nUse [green] cookietemple list [red]to display all template handles."
        )
        sys.exit(0)

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
                    templates_to_print.append(
                        [
                            templ["name"],
                            templ["handle"],
                            templ["long description"],
                            templ["available libraries"],
                            templ["version"],
                        ]
                    )
                else:
                    self.flatten_nested_dict(templ, templates_to_print)
        else:
            # a single template to append was reached
            templates_to_print.append(
                [
                    template_info_["name"],
                    template_info_["handle"],
                    template_info_["long description"],
                    template_info_["available libraries"],
                    template_info_["version"],
                ]
            )

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
                desc = desc[:last_space] + "\n" + desc[last_space + 1 :]
                cnt = 0
            elif desc[idx] == " ":
                last_space = idx
            cnt += 1
            idx += 1

        return desc

    @staticmethod
    def load_available_languages(ls: list) -> set:
        """
        Load all available languages cookietemple supports.
        NOTE: Assumption that all handles have two or three parts

        :param ls: The flattended list from the available templates dict
        :return: All available languages as a set
        """
        return {ls[1].split("-")[1] if len(ls[1].split("-")) == 2 else ls[1].split("-")[2] for ls in ls}
