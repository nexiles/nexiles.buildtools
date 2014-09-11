# -*- coding: utf-8 -*-
import logging, os, click, zipfile, shutil
import ConfigParser
from api import *

from fabric.api import task, env
from fabric.colors import green

logger = logging.getLogger("cli")

config = ConfigParser.ConfigParser()
config.read(os.path.expanduser("~/.nxdocserver"))

try:
    DOCSERVER_URL = config.get("Docserver", "url")
    DROPBOX = config.get("Docserver", "dropbox")
    username = config.get("Login", "user")
    password = config.get("Login", "password")

    folder_api = FolderAPI(DOCSERVER_URL, username, password)
    doc_api  = DocmetaAPI(DOCSERVER_URL, username, password)
    project_api  = ProjectAPI(DOCSERVER_URL, username, password)

except ConfigParser.NoSectionError:
     print("Error parsing config file at $HOME/.nxdocserver !")

@click.group()
@click.option("--debug", "-d", is_flag=True)
def cli(debug):
    logging.basicConfig(level=(debug and logging.DEBUG) or logging.ERROR, format="%(asctime)s [%(levelname)-7s] [line %(lineno)d] %(name)s: %(message)s")

################################################################################
# fabric task
################################################################################

@task
def publish_docs():
    """ create meta data for the documentation and copy its files to the Dropbox folder specified in $HOME/.nxdocserver
    """

    if "projectname_docs" in env:
        title = env.projectname_docs
    else:
        title = env.projectname

    project = project_api.find("title", title)
    if not project:
        project = publish_project(title)

    if "icon" in env:
        icon = env.icon
    else:
        icon = None

    publish(project["id"], title, env.package_version, env.doc_package, icon)

    print green("published docs.")

################################################################################

def publish(project, title, version, zip, icon=None):
    """ Before this command is run make sure the parent project exists
    """

    doc = Docmeta({
        "parent_id": project,
        "title": title,
        "version": version,
        "icon": icon
    })

    doc.save()

    # copy and unpack data
    basedir = os.path.join(DROPBOX, project, doc["id"])
    dst = os.path.join(basedir, doc["version"])
    zipfile.ZipFile(zip).extractall(dst)
    shutil.copyfile(zip, dst + ".zip")
    if icon:
        shutil.copyfile(icon, os.path.join(basdir, "icon.png"))

    return doc

def publish_project(title, github=None, project=None):
    """ Create meta data for the project and create a new directory in the Dropbox
        folder specified in $HOME/.nxdocserver
    """

    p = Project({
        "parent_id": project,
        "title": title,
        "github": github or "https://github.com/nexiles/" + title
    })

    # save meta data
    p.save()

    # create directory
    os.mkdir(os.path.join(DROPBOX, p["id"]))

    return p


################################################################################
# Docmeta C(R)UD commands
################################################################################

@click.command()
@click.option("--project", required=True, help="ID of the parent project")
@click.option("--title", required=True, help="Title of the documentation")
@click.option("--version", default="0.1.0", help="Version of the documentation")
@click.option("--zip", type=click.Path(exists=True), required=True, help="Location of the zip file")
@click.option("--icon", type=click.Path(exists=True), help="Location of the icon file")
def create_doc(**kwargs):

    publish(**kwargs)

@click.command()
@click.argument("name")
@click.option("--project", required=True, help="ID of the parent project of the object to update")
@click.option("--title", help="New title of the documentation")
@click.option("--version", help="New version of the documentation")
@click.option("--zip", type=click.Path(exists=True), help="Location of the new zip file")
@click.option("--icon", type=click.Path(exists=True), help="Location of the icon file")
def update_doc(name, project, title, version, zip, icon):

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
        shutil.copyfile(icon, os.path.join(basdir, "icon.png"))

    if title:
        # this will NOT update the id!
        doc["title"] = title

    doc.save()

@click.command()
@click.argument("name")
@click.option("--project", required=True, help="ID of the parent project")
def delete_doc(project, name):
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
@click.option("--project", help="ID of the parent project")
@click.option("--title", required=True, help="Title of the project")
@click.option("--github", help="GitHub URL of the project")
def create_project(**kwargs):

    publish_project(**kwargs)

@click.command()
@click.argument("name")
@click.option("--title", help="New title of the project")
@click.option("--github", help="New GitHub URL of the project")
def update_project(name, **kw):
    kw = dict((k, v) for k, v in kw.items() if v)
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

@click.command()
def test():

    # list all projects
    for p in project_api.list():
        print p["title"] + " " + p["state"] + " " + p["github"]


    # TEST PROJECTS API
    # -----------------------------

    # create a project
    p = Project({
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
    d = Docmeta({
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


cli.add_command(create_doc)
cli.add_command(update_doc)
cli.add_command(delete_doc)
cli.add_command(create_project)
cli.add_command(update_project)
cli.add_command(delete_project)
cli.add_command(test)

# vim: set ft=python ts=4 sw=4 expandtab :
