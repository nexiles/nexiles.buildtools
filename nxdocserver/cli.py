# -*- coding: utf-8 -*-
import os
import sys
import click
import zipfile
import shutil
import logging
import ConfigParser

from fabric import colors

import api
import log
import conf
import tasks

logger = log.logger

@click.group()
@click.option("--debug", "-d", is_flag=True)
def cli(debug):
    log.setup_logging(level=debug and logging.DEBUG or logging.ERROR)

@click.command()
def version():
    """print the version and exit."""
    import pkg_resources
    print(colors.green("nxdocserver {}".format(pkg_resources.get_distribution("nxdocserver").version)))

################################################################################
# Docmeta C(R)UD commands
################################################################################

@click.command()
def list_docs(**kwargs):
    """List all documentation on the server."""
    format_string = "{title:<45} {state:<15} {creator.fullname:<20} {version:<15} {visibility:<10} {modification_date}"
    for p in doc_api.list():
        print(p.format(format_string))

@click.command()
@click.option("--project", required=True, help="ID of the parent project")
@click.option("--title", required=True, help="Title of the documentation")
@click.option("--version", default="0.1.0", help="Version of the documentation")
@click.option("--zip", type=click.Path(exists=True), required=True, help="Location of the zip file")
@click.option("--icon", type=click.Path(exists=True), help="Location of the icon file")
def create_doc(**kwargs):
    """Create a new documentation."""
    tasks.publish_docs(**kwargs)

@click.command()
@click.argument("name")
@click.option("--project", required=True, help="ID of the parent project of the object to update")
@click.option("--title", help="New title of the documentation")
@click.option("--version", help="New version of the documentation")
@click.option("--zip", type=click.Path(exists=True), help="Location of the new zip file")
@click.option("--icon", type=click.Path(exists=True), help="Location of the icon file")
def update_doc(name, project, title, version, zip, icon):
    """Update a existing documentation."""
    logger.debug("update_doc: %s %s %s %s %s %s", name, project, title, version, zip, icon)

    doc = project_api.find_docmeta(project, name)

    if not doc:
        raise click.ClickException("Documentation not found. Aborting")

    basedir = os.path.join(DROPBOX, project, doc["id"])

    if version:
        src = os.path.join(basedir, doc["version"])
        dst = os.path.join(basedir, version)

        # rename html folder
        shutil.move(src, dst)

        # rename zip file
        shutil.move(src + ".zip", dst + ".zip")

        doc["version"] = version

    dst = os.path.join(basedir, doc["version"])

    if zip:
        # copy and extract new file
        zipfile.ZipFile(zip).extractall(dst)
        shutil.copyfile(zip, dst + ".zip")

    if icon:
        # copy icon to same directory as before
        shutil.copyfile(icon, os.path.join(basedir, "icon.png"))

    if title:
        # this will NOT update the id!
        doc["title"] = title

    doc.save()

@click.command()
@click.argument("name")
@click.option("--project", required=True, help="ID of the parent project")
def delete_doc(project, name):
    """Delete documentation."""
    doc = project_api.find_docmeta(project, name)

    if not doc:
        raise click.ClickException("Documentation not found. Aborting")

    # remove meta data
    doc.delete()

    # remove files
    dst = os.path.join(DROPBOX, project, doc["id"])
    if not os.path.exists(dst):
        raise click.ClickException("Documentation files not found")
    shutil.rmtree(dst)


################################################################################
# Project C(R)UD commands
################################################################################

@click.command()
def list_projects(**kwargs):
    """List all projects on the server."""
    print(colors.green("{title:<40} {state:<15} {creator:<20} {github}".format(title="Project Title", state="Project State", creator="Project Creator", github="GitHub URL")))
    for p in project_api.list():
        print(p.format("{title:<40} {state:<15} {creator.fullname:<20} {github}"))

@click.command()
@click.option("--project", help="ID of the parent project")
@click.option("--title", required=True, help="Title of the project")
@click.option("--github", help="GitHub URL of the project")
def create_project(**kwargs):
    """Create a new project."""
    tasks.publish_project(**kwargs)

@click.command()
@click.argument("name")
@click.option("--title", help="New title of the project")
@click.option("--github", help="New GitHub URL of the project")
def update_project(name, **kw):
    "Update a existing project."
    if not kw:
        raise click.ClickException("Nothing to update. Aborting")

    project = project_api.find("id", name)
    if not project:
        raise click.ClickException("Project not found. Aborting")

    project.update(kw)
    project.save()

@click.command()
@click.argument("name")
def delete_project(name):
    "Delete a project."
    project = project_api.find("id", name)
    if not project:
        raise click.ClickException("Project not found. Aborting")

    # remove meta data
    project.delete()

    # remove the directory and all files
    dst = os.path.join(DROPBOX, name)
    if not os.path.exists(dst):
        raise click.ClickException("Project files not found")
    shutil.rmtree(dst)

def test():

    # list all projects
    for p in project_api.list():
        print p["title"] + " " + p["state"] + " " + p["github"]

    # TEST PROJECTS API
    # -----------------------------

    # create a project
    p = api.Project({
        "title": "Test Project",
        "github": "https://github.com/nexiles/nexiles.plone.docs"
    })

    p.save()

    # update
    p["github"] = "http://google.de"
    p.save()
    assert p["github"] == "http://google.de"

    # TEST DOCMETAS
    # -----------------------------

    # create a project
    d = api.Docmeta({
        "parent_id": p["id"],
        "title": "Test Doc",
        "version": "0.0.1",
        "icon": None
    })
    d.save()

    # update
    d["doc_icon"] = "foo.jpg"
    d.save()
    assert d["doc_icon"].endswith("foo.jpg")

    # CLEANUP
    # -------

    # delete docmeta
    d.delete()

    # delete project
    p.delete()

    print "Test completed successfully"

config = conf.get_configuration()

DOCSERVER_URL = config.docserver_url
DROPBOX       = config.docserver_dropbox
username      = config.login_username
password      = config.login_password

folder_api  = api.FolderAPI(DOCSERVER_URL, username, password)
doc_api     = api.DocmetaAPI(DOCSERVER_URL, username, password)
project_api = api.ProjectAPI(DOCSERVER_URL, username, password)

cli.add_command(version)
cli.add_command(list_docs)
cli.add_command(create_doc)
cli.add_command(update_doc)
cli.add_command(delete_doc)
cli.add_command(list_projects)
cli.add_command(create_project)
cli.add_command(update_project)
cli.add_command(delete_project)

# vim: set ft=python ts=4 sw=4 expandtab :
