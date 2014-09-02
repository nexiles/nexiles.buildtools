# -*- coding: utf-8 -*-
import logging, os, click, zipfile, shutil
import ConfigParser
from resources import *

config = ConfigParser.ConfigParser()
config.read(os.path.expanduser("~/.nxdocserver"))
DOCSERVER_URL = config.get("Docserver", "url")
DROPBOX = config.get("Docserver", "dropbox")
username = config.get("Login", "user")
password = config.get("Login", "password")

plone_api = API(DOCSERVER_URL, "plone", username, password)
docs_api  = API(DOCSERVER_URL, "docs", username, password)

folders   = PloneFolders(plone_api)
projects  = Projects(docs_api)
docmetas  = Docmetas(docs_api)

@click.group()
@click.option("--debug", "-d", is_flag=True)
def cli(debug):
    logging.basicConfig(level=(debug and logging.DEBUG) or logging.ERROR, format="%(asctime)s [%(levelname)-7s] [line %(lineno)d] %(name)s: %(message)s")

################################################################################
# Docmeta C(R)UD commands
################################################################################

@click.command()
@click.option("--project", required=True, help="ID of the parent project")
@click.option("--title", required=True, help="Title of the documentation")
@click.option("--version", default="0.1.0", help="Version of the documentation")
@click.option("--zip", type=click.Path(exists=True), required=True, help="Location of the zip file")
@click.option("--icon", type=click.Path(exists=True), help="Location of the icon file")
def create_doc(project, title, version, zip, icon):
    parent = projects.find("id", project)
    if not parent:
        raise click.ClickException("Parent project not found. Aborting")

    # Check for duplicates
    for doc in parent["docs"]:
        if doc["title"] == title and doc["version"] == version:
            raise click.ClickException("Documentation already exists. Aborting")

    # create meta data
    doc = docmetas.create(parent["uid"], title=title, version=version)

    # copy and unpack data
    basedir = os.path.join(DROPBOX, project, doc["id"])
    dst = os.path.join(basedir, version)
    zipfile.ZipFile(zip).extractall(dst)
    shutil.copyfile(zip, dst + ".zip")
    if icon:
        shutil.copyfile(icon, os.path.join(basdir, "icon.png"))

        # add the icon to the docmeta
        docmetas.update(doc["uid"], doc_icon=os.path.join(project, doc["id"], "icon.png"))

@click.command()
@click.argument("name")
@click.option("--project", required=True, help="ID of the parent project of the object to update")
@click.option("--title", help="New title of the documentation")
@click.option("--version", help="New version of the documentation")
@click.option("--zip", type=click.Path(exists=True), help="Location of the new zip file")
@click.option("--icon", type=click.Path(exists=True), help="Location of the icon file")
def update_doc(name, project, title, version, zip, icon):

    doc = projects.find_docmeta(name, project)

    # Check for duplicates
    # if kw["title"] or kw["version"]:
    #     project = projects.find("id", project)
    #     for d in project["docs"]:
    #         if d["title"] == (kw["title"] or doc["title"]) and d["version"] == (kw["version"] or doc["version"]):
    #             raise click.ClickException("Documentation already exists. Aborting")

    kw = dict()
    basedir = os.path.join(DROPBOX, project, doc["id"])

    if version:
        kw["version"] = version

        src = os.path.join(basedir, doc["version"])
        dst = os.path.join(basedir, version)

        # rename html folder
        shutil.move(src, dst)

        # rename zip file
        shutil.move(src + ".zip", dst + ".zip")

    dst = os.path.join(basedir, (version or doc["version"]))

    if zip:
        kw["zip"] = zip

        # copy and extract new file
        zipfile.ZipFile(kw["zip"]).extractall(dst)
        shutil.copyfile(kw["zip"], dst + ".zip")

    if icon:
        # copy icon to same directory as before
        shutil.copyfile(icon, os.path.join(basdir, "icon.png"))

    if title:
        # this will NOT update the id!
        kw["title"] = title

    docmetas.update(doc["uid"], **kw)

@click.command()
@click.argument("name")
@click.option("--project", required=True, help="ID of the parent project")
def delete_doc(project, name):
    doc = projects.find_docmeta(name, project)

    # remove meta data
    docmetas.delete(doc["uid"])

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
def create_project(project, **kw):

    # Check for duplicates
    if projects.find("title", kw["title"]):
            raise click.ClickException("A Project with this title already exists")

    if project:
        # nested project
        parent = projects.find("id", project)
    else:
        # add to documentation folder as default
        parent = folders.find("title", "Documentation")

    if not parent:
        raise click.ClickException("Parent not found. Aborting")

    if not kw["github"]:
        kw["github"] = "https://github.com/nexiles/" + kw["title"]

    # create meta data
    project = projects.create(parent["uid"], **kw)

    # create directory
    os.mkdir(os.path.join(DROPBOX, project["id"]))

@click.command()
@click.argument("name")
@click.option("--title", help="New title of the project")
@click.option("--github", help="New GitHub URL of the project")
def update_project(name, **kw):
    kw = dict((k, v) for k, v in kw.items() if v)
    if not kw:
        raise click.ClickException("Nothing to update. Aborting")

    # Check for duplicates
    # if kw["title"] and projects.find("title", kw["title"]):
    #     raise click.ClickException("A Project with this title already exists. Aborting")

    project = projects.find("id", name)
    if not project:
        raise click.ClickException("Project not found. Aborting")

    projects.update(project["uid"], **kw)

@click.command()
@click.argument("name")
def delete_project(name):
    project = projects.find("id", name)
    if not project:
        raise click.ClickException("Project not found. Aborting")

    # remove meta data
    projects.delete(project["uid"])

    # remove the directory and all files
    dst = os.path.join(DROPBOX, name)
    if not os.path.exists(dst):
        raise click.ClickException("Project files not found")
    shutil.rmtree(dst)

@click.command()
def test():

    # list all projects
    for p in projects:
        print "{title} {state} {github}".format(**p)

    print "Nexiles Gateway" in projects

    # TEST PROJECTS API
    # -----------------------------

    # create a project
    parent_uid = folders.find("title", "Documentation")["uid"]
    p = projects.create(parent_uid, title="Test Project", github="https://github.com/nexiles/nexiles.plone.docs")

    # update
    p = projects.update(p["uid"], github="http://google.de")
    assert p["github"] == "http://google.de"

    # TEST DOCMETAS
    # -----------------------------

    # create a project
    d = docmetas.create(
        p["uid"],
        title="Test Doc",
        version="0.0.1",
        doc_icon=None)

    # update
    d = docmetas.update(d["uid"], doc_icon="foo.jpg")
    assert d["doc_icon"].endswith("foo.jpg")

    # CLEANUP
    # -------

    # delete docmeta
    docmetas.delete(d["uid"])

    # delete project
    projects.delete(p["uid"])


cli.add_command(create_doc)
cli.add_command(update_doc)
cli.add_command(delete_doc)
cli.add_command(create_project)
cli.add_command(update_project)
cli.add_command(delete_project)
cli.add_command(test)

# vim: set ft=python ts=4 sw=4 expandtab :
