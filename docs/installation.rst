.. highlight:: shell

.. _installation:

============
Installation
============


Stable release
--------------

To install cookietemple, run this command in your terminal:

.. code-block:: console

    $ pip install cookietemple

This is the preferred method to install cookietemple, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for cookietemple can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/cookiejar/cookietemple

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/cookiejar/cookietemple/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ pip install .

Alternatively you can also install it using the Makefile:

.. code-block:: console

    $ make install


.. _Github repo: https://github.com/cookiejardealer/cookietemple
.. _tarball: https://github.com/cookiejardealer/cookietemple/tarball/master

Upgrading cookietemple
------------------------

Every time cookietemple is run it will automatically check whether a newer version has been released on PyPI.
If a new version has been released you will be informed. To upgrade cookietemple either run::

    $ pip install --upgrade cookietemple

or by invoking::

    $ cookietemple upgrade

For more information please visit :ref:`upgrade`.

Windows Installation
--------------------

Cookietemple exceeds the standard windows path length limit of 260 characters.
In order to correctly install cookietemple the registry has to be adapted.
To open the registry editor run:

.. code-block:: console

    $ regedit

in your command prompt or directly open it through windows search bar.

**Consider backing up your current registry state** as changes in the registry can always cause problems resulting in
your OS not running correctly. You can either export the complete registry by selecting File > Export ... and setting
the Export Range flag to 'All' or choose to export only selected branches.

Next find the key **'LongPathsEnabled'** under

.. code-block:: rst

    HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem

and change its 'Value Data' from '0' to '1'.

Click 'OK' and close regedit. Continue installing cookietemple.
