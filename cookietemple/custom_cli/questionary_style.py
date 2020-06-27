from prompt_toolkit.styles import Style

cookietemple_style = Style([
    ('qmark', 'fg:#0000FF bold'),       # token in front of the question
    ('question', 'bold'),               # question text
    ('answer', 'fg:#008000 bold'),      # submitted answer text behind the question
    ('pointer', 'fg:#0000FF bold'),     # pointer used in select and checkbox prompts
    ('highlighted', 'fg:#0000FF bold'), # pointed-at choice in select and checkbox prompts
    ('selected', 'fg:#008000'),         # style for a selected item of a checkbox
    ('separator', 'fg:#cc5454'),        # separator in lists
    ('instruction', ''),                # user instructions for select, rawselect, checkbox
    ('text', ''),                       # plain text
    ('disabled', 'fg:#858585 italic')   # disabled choices for select and checkbox prompts
])
