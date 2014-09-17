# -*- coding: utf-8 -*-
#
# File: tasks.py
#
# Copyright (c) nexiles GmbH
#
__author__    = """Stefan Eletzhofer <se@nexiles.de>"""
__docformat__ = 'plaintext'
__revision__  = "$Revision: $"
__version__   = '$Revision: $'[11:-2]


import os
import sys
import shutil

from fabric import colors
from fabric.api import task, env
from fabric.api import lcd
from fabric.api import local

import conf
import api
import cli

@task
def publish_docs():
    """ create meta data for the documentation and copy its files to the Dropbox folder specified in $HOME/.nxdocserver
    """

    if "projectname_docs" in env:
        title = env.projectname_docs
    else:
        title = env.projectname

    if not os.path.exists(env.doc_package):
        print colors.red("Documentation package found: %s" % env.doc_package)
        sys.exit(10)

    project = cli.project_api.find("title", title)
    if not project:
        project = publish_project(title)

    if "icon" in env:
        icon = env.icon
    else:
        icon = None

    publish_doc(project["id"], title, env.package_version, env.doc_package, icon)

    print colors.green("published docs.")

@task
def update_docs():
    if "projectname_docs" in env:
        title = env.projectname_docs
    else:
        title = env.projectname

    if "icon" in env:
        icon = env.icon
    else:
        icon = None

    if not os.path.exists(env.doc_package):
        print colors.red("Documentation package found: %s" % env.doc_package)
        sys.exit(10)

    project = cli.project_api.find("title", title)
    if not project:
        print colors.red("Project not found: %s" % title)
        sys.exit(10)

    doc = cli.project_api.find_doc_by_version(title, env.package_version)
    if not doc:
        print colors.red("Documentation for version not found: %s" % env.package_version)
        sys.exit(10)

    copy_files(project["id"], doc, env.doc_package, icon)

################################################################################

def publish_doc(project, title, version, zip, icon=None):
    """ Before this command is run make sure the parent project exists
    """
    doc = api.Docmeta({
        "parent_id": project,
        "title": title,
        "version": version,
        "icon": icon
    })

    doc.save()

    copy_files(project, doc, zip)

    return doc

def copy_files(project, doc, doc_package, icon=None):
    config = conf.get_configuration()
    # copy and unpack data
    basedir = os.path.join(config.docserver_dropbox, project, doc["id"])
    dst = os.path.join(basedir, doc["version"])
    local("cp {} {}.zip".format(doc_package, dst))
    local("mkdir -p {}".format(dst))
    with lcd(dst):
        local("unzip {}".format(doc_package))
    if icon:
        shutil.copyfile(icon, os.path.join(basedir, "icon.png"))
        local("cp {} {}/icon.png".format(icon, basedir))

def publish_project(title, github=None, project=None):
    """ Create meta data for the project and create a new directory in the Dropbox
        folder specified in $HOME/.nxdocserver
    """

    config = conf.get_configuration()

    p = api.Project({
        "parent_id": project,
        "title": title,
        "github": github or "https://github.com/nexiles/" + title
    })

    # save meta data
    p.save()

    # create directory
    local("mkdir -p {}".format(os.path.join(config.docserver_dropbox, p["id"])))

    return p


# vim: set ft=python ts=4 sw=4 expandtab :
