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
import zipfile
import shutil
import logging

from fabric.api import task, env
from fabric import colors

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

    project = cli.project_api.find("title", title)
    if not project:
        project = publish_project(title)

    if "icon" in env:
        icon = env.icon
    else:
        icon = None

    publish(project["id"], title, env.package_version, env.doc_package, icon)

    print colors.green("published docs.")

################################################################################

def publish(project, title, version, zip, icon=None):
    """ Before this command is run make sure the parent project exists
    """

    config = conf.get_configuration()

    doc = api.Docmeta({
        "parent_id": project,
        "title": title,
        "version": version,
        "icon": icon
    })

    doc.save()

    # copy and unpack data
    basedir = os.path.join(config.docserver_dropbox, project, doc["id"])
    dst = os.path.join(basedir, doc["version"])
    zipfile.ZipFile(zip).extractall(dst)
    shutil.copyfile(zip, dst + ".zip")
    if icon:
        shutil.copyfile(icon, os.path.join(basedir, "icon.png"))

    return doc

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
    os.mkdir(os.path.join(config.docserver_dropbox, p["id"]))

    return p


# vim: set ft=python ts=4 sw=4 expandtab :
