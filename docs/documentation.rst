==========================
How to build Documentation
==========================

:Date: |today|


Abstract
========

This is a quick guide to create documentation.

Introduction
============

We at nexiles make documentation with Sphinx_ and use the Bootstrap_ theme with
some additional styling.

docs.nexiles.com
================

Our documentation is hosted on https://docs.nexiles.com.

The meta data is managed via Plone and the documentation files are pushed to the
server via the `docserver` Dropbox folder.
Access to specific documentation is handled by the privileges of the Plone users
that are synchronized with our Active Directory Server.

Distributing Documentation
==========================

To bring your docs to https://docs.nexiles.com, you need to have the
following prerequisites:

#. Sphinx_ and Fabric_ is installed. See `requirements.txt` inside this
   project for version infos.

#. You have an Active Directory account that is enabled for `docs.nexiles.com`
   and you are in the group `Developers`.

#. The documentation is located at the `docs` folder inside your project.

#. You have `nexiles.buildtools` cloned and located at
   `~/develop/nexiles/nexiles.buildtools`

#. You have installed the `nxdocserver` package


The next step is to customize your `fabfile.py` of your project.
You can extend your `fabfile.py` as follows::

    import os
    import sys

    from fabric.api import env

    # version of the project (can also be in another file)
    __version__ = "0.1"
    __date__ = "2013-04-23"
    __build__ = 0

    # add the nexiles.buildtools `fab` package to the sys.path
    sys.path.append(os.path.expanduser("~/develop/nexiles/nexiles.buildtools/fab"))

    # set the project name
    env.projectname = "nexiles.buildtools"

    # set a version file
    env.version_file = os.path.abspath("%s/fabfile.py" % os.getcwd())

    # run setup steps
    from nxfab import setup_version, setup_env
    setup_version()
    setup_env()

    # import the documentation tasks
    from docs import build_docs, package_docs
    from nxdocserver.cli import publish_docs


Now you can build your documentation like this::

    $ fab build_docs

Then package the built files like this::

    $ fab package_docs

And distribute it to `docs.nexiles.com` like this::

    $ fab publish_docs

.. _Sphinx: http://sphinx.pocoo.org/
.. _Fabric: https://github.com/fabric/fabric
.. _NxSphinx: https://github.com/nexiles/NxSphinx
.. _nexiles.buildtools: https://github.com/nexiles/nexiles.buildtools
.. _Bootstrap: https://pypi.python.org/pypi/sphinx-bootstrap-theme/

.. vim: set ft=rst ts=4 sw=4 expandtab tw=78 :
