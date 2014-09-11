# -*- coding: utf-8 -*-

# copyright (c) 2013 nexiles GmbH

import os
from contextlib import nested

from fabric.api import task
from fabric.api import env
from fabric.api import lcd
from fabric.api import local, run
from fabric.api import prompt
from fabric.api import abort
from fabric.api import prefix
from fabric.colors import green
from fabric.api import settings, hide


from version import get_version
from build import zip_package

__all__ = ["build_docs", "package_docs"]


def make():
    with nested(lcd("docs"), settings(hide("stdout"))):
        local("make html")

@task
def build_docs():
    """ build the documentation with sphinx
    """
    if "docs_build_venv" in env:
        with prefix("source %(docs_build_venv)s/bin/activate" % env):
            make()
    else:
        make()

    print green("finished building the documentation")

@task
def package_docs():
    """package documentation"""
    zip_package(env.doc_package, "docs/_build/html", ".")
    print green("created %(doc_package)s." % env)

# vim: set ft=python ts=4 sw=4 expandtab :
