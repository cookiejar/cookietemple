import logging
import sys

import click
import questionary
from prompt_toolkit.styles import Style

cookietemple_style = Style([
    ('qmark', 'fg:#0000FF bold'),  # token in front of the question
    ('question', 'bold'),  # question text
    ('answer', 'fg:#008000 bold'),  # submitted answer text behind the question
    ('pointer', 'fg:#0000FF bold'),  # pointer used in select and checkbox prompts
    ('highlighted', 'fg:#0000FF bold'),  # pointed-at choice in select and checkbox prompts
    ('selected', 'fg:#008000'),  # style for a selected item of a checkbox
    ('separator', 'fg:#cc5454'),  # separator in lists
    ('instruction', ''),  # user instructions for select, rawselect, checkbox
    ('text', ''),  # plain text
    ('disabled', 'fg:#FF0000 italic')  # disabled choices for select and checkbox prompts
])


def cookietemple_questionary(function: str, question: str, default_value: str = None, choices: list = None) -> str:
    """
    Custom selection based on Questionary. Handles keyboard interrupts and default values.

    :param function: The function of questionary to call (e.g. select or text). See https://github.com/tmbo/questionary for all available functions.
    :param choices: List of all possible choices.
    :param question: The question to prompt for. Should not include default values or colons.
    :param default_value: A set default value, which will be chosen if the user does not enter anything.
    :return: The chosen answer.
    """
    try:
        if choices:
            if default_value not in choices:
                logging.debug(f'Default value {default_value} is not in the set of choices!')
            answer = getattr(questionary, function)(f'{question}: ', choices=choices, style=cookietemple_style).unsafe_ask()
        else:
            if function == 'password':
                answer = ''
                while not answer or answer == '':
                    answer = getattr(questionary, function)(f'{question}: ', style=cookietemple_style).unsafe_ask()
            else:
                if not default_value:
                    logging.debug('Tried to utilize default value in questionary prompt, but is None! Please set a default value.')
                    default_value = ''
                answer = getattr(questionary, function)(f'{question} [{default_value}]: ', style=cookietemple_style).unsafe_ask()

    except KeyboardInterrupt:
        click.echo(click.style('Aborted by user!', fg='red'))
        sys.exit(1)
    if not answer or answer == '':
        answer = default_value

    return answer
