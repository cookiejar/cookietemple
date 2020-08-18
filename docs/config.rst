.. _config:

=======================
Configure cookietemple
=======================

To prevent frequent prompts for information, which rarely or never changes at all such as the full name, email or Github name of the user cookietemple uses a configuration file.
Moreover, the personal access token associated with the Github username is stored encrypted to increase the security even if malicious attackers already have access to your personal computer.
The creation of projects with cookietemple requires a configuration file. A personal access token is not required, if Github support is not used.
The configuration file is saved operating system dependent in the usual config file locations (~/.config/cookietemple on Unix, C:\Users\Username\AppData\Local\cookietemple\cookietemple).

Invoke cookietemple config *via*

.. code-block:: console
    :linenos:

    $ cookietemple config <all/general/pat>

cookietemple config all
------------------------

If :code:`cookietemple config all` is called, the options :code:`general` and afterwards :code:`pat` are called.

cookietemple config general
------------------------------

:code:`cookietemple config general` prompts for the full name, email address and Github username of the user. If you are not using Github simply keep the default value.
These attributes are shared by all templates and therefore should only be set once. If you need to update these attributes naturally rerun the command.

cookietemple config pat
----------------------------

cookietemple's Github support requires access to your Github repositories to create repositories, add issues labels and set branch protection rules.
Github manages these access rights through Personal Access Tokens (PAT).
If you are using cookietemple's Github support for the first time :code:`cookietemple config pat` will be run and you will be prompted for your Github PAT.
Please refer to the `official documentation <https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line>`_ on how to create one.
cookietemple only requires ``repo`` access, so you only need to tick this box. However, if you want to use cookietemple's sync feature on organisation repositories,
you also need to tick :code:`admin:org`. This ensures that your PAT would not even allow for the deletion of repositories.
cookietemple then encrypts the Personal Access Token, adds the encrypted token to the :code:`cookietemple_conf.cfg` file (OS dependent stored) and saves the key locally in a hidden place.
This is safer than Github's official way, which recommends the usage of environment variables or Github Credentials, which both save the token in plaintext.
It is still strongly adviced to secure your personal computer and not allow any foe to get access.
If you create a second project using cookietemple at a later stage, you will not be prompted again for your Github username, nor your Personal Access Token.

Updating a personal access token
------------------------------------

If you for any reason need to regenerate your PAT rerun :code:`cookietemple config pat`. Ensure that your Github username still matches.
If not you should also update your Github username *via* :code:`cookietemple config general`.
Additionally, any of your already created projects may still feature your old PAT and you may therefore run into issues when attempting to push.
Hence, you must also `update your remote URL <https://help.github.com/en/github/using-git/changing-a-remotes-url>`_ for those projects!
