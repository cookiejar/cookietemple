.. _upgrade:

=====================
Upgrade cookietemple
=====================

Every time cookietemple is run it will automatically contact PyPI to check whether the locally installed version of cookietemple is the latest version available.
If a new version is available cookietemple can be trivially upgraded. Note that ``pip`` must be available in your ``PATH``.
It is advised not to mix installations using setuptools directly and pip. If you are not a developer of cookietemple this should not concern you.

Usage
--------

.. code-block::

    $ cookietemple upgrade
