# -*- coding: utf-8 -*-

# copyright (c) 2013 nexiles GmbH

import os

from fabric.api import task
from fabric.api import env
from fabric.api import lcd
from fabric.api import local
from fabric.api import prompt
from fabric.api import abort
from fabric.colors import green

from version import get_version

__all__ = ["build_docs", "publish_docs"]

HOST = "docs.nexiles.com"

@task
def build_docs():
    """ build the documentation with sphinx
    """

    with lcd("docs"):
        local("make html")
    return green("finished building the documentation")

@task
def publish_docs(version=None, internal=True):
    """ publish the documentation
    """
    build_dir = os.path.join("docs", "_build", "html")
    if not os.path.exists(build_dir):
        abort("Please build the docs first")

    docs_dir = "/srv/docs/%s" % (internal and "internal" or "public")
    doc_root = "%s/%s" % (docs_dir, env.projectname)

    if not version:
        version_info = get_version()
        prompt("Which version: ", default=version_info["version"], key="package_version")
    else:
        env.package_version=version

    with lcd("docs"):
        doc_path = "%s/%s" % (doc_root, env.package_version)
        local("rsync -avz --del _build/html/ %s:%s" % (HOST, doc_path))
        local("ssh %s 'cd %s && rm -f latest && ln -s %s latest'" % (HOST, doc_root, env.package_version))

# vim: set ft=python ts=4 sw=4 expandtab :
