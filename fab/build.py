import os

from contextlib import nested

from fabric.api import task
from fabric.api import local
#from fabric.api import run
#from fabric.api import cd
from fabric.api import lcd
#from fabric.api import prefix
#from fabric.api import put
from fabric.api import env
from fabric.api import settings, hide
#from fabric.api import prompt
from fabric.colors import green, yellow, red
from fabric.contrib.console import confirm

from nxfab import eggs
from manifest import make_manifest_file

__all__ = ["build_templates", "build_static", "build_eggs"]


def zip_package(package, directory, root):
    """create a package zip file"""
    with nested(lcd(directory), settings(hide("stdout"))):
        local("zip -r %(package)s %(root)s" % locals())

@task
def build_templates(directory="src"):
    """build_templates -- package the templates"""
    zip_package(env.templates_package, directory, "templates")

@task
def build_static(directory="src"):
    """build_static -- package static files"""
    zip_package(env.static_package, directory, "static")

@task
def build_eggs():
    """build package egges"""
    for package, egg in eggs():
        print yellow("building egg for %s" % package)
        with lcd("src/"+ package):

            with settings(hide("stdout")):
                local("nxjython --wt setup.py bdist_egg --exclude-source")

            # add manifest
            mf = make_manifest_file(package, egg)

            resources = package.split(".") + ["resources",]
            resources = os.path.join(*resources)

            if not os.path.exists(os.path.join(env.lcwd, resources)):
                print red("resources dir missing: ") + yellow(resources)
                print red("creating resources dir for package: ") + yellow(package)
                local("mkdir -p %s" % resources)

            # copy manifest file
            local("cp %s %s/manifest.json" % (mf, resources))

            # package resources
            local("zip -ur dist/%s %s" % (egg, resources))

@task
def build_app(version=None, bump_vers=False):
    """Deploy nexiles.gateway.attributeservice to server"""
    raise NotImplementedError()
    if bump_vers:
        bump_version()

    print "building version: " + yellow(env.package_version)

    app_package = get_app_package()

    with lcd("src/nexiles.rotator.lotapp"):
        local("coffee --output static/ -c src/")
        with lcd("static"):
            for folder in "css images".split():
                local("cp -r %s build/App/production" % folder)
            local("sencha app build")
            with lcd("build/App/production"):
                local("zip -r %s . -x \*.sass-cache\*" % app_package)

    print "built version: ", green(app_package)


# vim: set ft=python ts=4 sw=4 expandtab :
