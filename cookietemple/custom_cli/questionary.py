import logging
import sys
from typing import Dict, List, Optional, Union

import questionary
from prompt_toolkit.styles import Style  # type: ignore

from cookietemple.util.rich import console

log = logging.getLogger(__name__)


cookietemple_style = Style(
    [
        ("qmark", "fg:#0000FF bold"),  # token in front of the question
        ("question", "bold"),  # question text
        ("answer", "fg:#008000 bold"),  # submitted answer text behind the question
        ("pointer", "fg:#0000FF bold"),  # pointer used in select and checkbox prompts
        ("highlighted", "fg:#0000FF bold"),  # pointed-at choice in select and checkbox prompts
        ("selected", "fg:#008000"),  # style for a selected item of a checkbox
        ("separator", "fg:#cc5454"),  # separator in lists
        ("instruction", ""),  # user instructions for select, rawselect, checkbox
        ("text", ""),  # plain text
        ("disabled", "fg:#FF0000 italic"),  # disabled choices for select and checkbox prompts
    ]
)


def cookietemple_questionary_or_dot_cookietemple(
    function: str,
    question: str,
    choices: Optional[List[str]] = None,
    default: Optional[str] = None,
    dot_cookietemple: Dict = None,
    to_get_property: str = None,
) -> Union[str, bool]:
    """
    Custom selection based on Questionary. Handles keyboard interrupts and default values.

    :param function: The function of questionary to call (e.g. select or text). See https://github.com/tmbo/questionary for all available functions.
    :param choices: List of all possible choices.
    :param question: The question to prompt for. Should not include default values or colons.
    :param default: A set default value, which will be chosen if the user does not enter anything.
    :param dot_cookietemple: A dictionary, which contains the whole .cookietemple.yml content
    :param to_get_property: A key, which must be in the dot_cookietemple file, which is used to fetch the read in value from the .cookietemple.yml file
    :return: The chosen answer.
    """
    # First check whether a dot_cookietemple was passed and whether it contains the desired property -> return it if so
    try:
        if dot_cookietemple:
            if to_get_property in dot_cookietemple:
                return dot_cookietemple[to_get_property]
    except KeyError:
        log.debug(
            f".cookietemple.yml file was passed when creating a project, but key {to_get_property}"
            f" does not exist in the dot_cookietemple dictionary! Assigning default {default} to {to_get_property}."
        )
        return default  # type: ignore

    # There is no .cookietemple.yml file aka dot_cookietemple dict passed -> ask for the properties
    answer: Optional[str] = ""
    try:
        if function == "select":
            if default not in choices:  # type: ignore
                log.debug(f"Default value {default} is not in the set of choices!")
            answer = getattr(questionary, function)(
                f"{question}: ", choices=choices, style=cookietemple_style
            ).unsafe_ask()
        elif function == "password":
            while not answer or answer == "":
                answer = getattr(questionary, function)(f"{question}: ", style=cookietemple_style).unsafe_ask()
        elif function == "text":
            if not default:
                log.debug(
                    "Tried to utilize default value in questionary prompt, but is None! Please set a default value."
                )
                default = ""
            answer = getattr(questionary, function)(f"{question} [{default}]: ", style=cookietemple_style).unsafe_ask()
        elif function == "confirm":
            default_value_bool = True if default == "Yes" or default == "yes" else False
            answer = getattr(questionary, function)(
                f"{question} [{default}]: ", style=cookietemple_style, default=default_value_bool
            ).unsafe_ask()
        else:
            log.debug(f"Unsupported questionary function {function} used!")

    except KeyboardInterrupt:
        console.print("[bold red] Aborted!")
        sys.exit(1)
    if answer is None or answer == "":
        answer = default

    log.debug(f"User was asked the question: ||{question}|| as: {function}")
    log.debug(f"User selected {answer}")

    return answer  # type: ignore
