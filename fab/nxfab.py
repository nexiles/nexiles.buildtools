import os
import zipfile
import datetime
from hashlib import sha256

try:
    import json
except ImportError:
    import simplejson as json

from fabric.api import task
from fabric.api import local
from fabric.api import run
from fabric.api import cd
from fabric.api import lcd
from fabric.api import prefix
from fabric.api import put
from fabric.api import env
from fabric.api import prompt
from fabric.colors import green, yellow, red
from fabric.contrib.console import confirm

from version import get_version

__all__ = ["eggs", "setup_env", "setup_version", "print_env"]

def eggs():
    """eggs -> generator

    A generator which yields package name, egg tuples.
    """
    for package in env.packages:
        egg = egg_for_package(package)
        yield package, egg

def egg_for_package(p):
    """egg_for_package(p) -> string

    Returns egg name from package name.
    """
    if not p.endswith("egg"):
        egg = "%s-VERSION-py2.5.egg" % p
    else:
        egg = p
    return egg.replace("VERSION", env.package_version)

def setup_version(version=None, ask=False):
    if not version:
        version_info = get_version()
        if ask:
            prompt("Which version: ", default=version_info["version"], key="package_version")
        else:
            env.package_version = version_info["version"]
    else:
        env.package_version = version

def setup_env():
    """setup_env -- set up fab global environment.

    XXX: This should use configparser to fetch settings from projectname.ini or project.ini
    """
    def versioned_file(fn, ext="tgz"):
        s = "%(projectname)s-" + fn + "-%(package_version)s." + ext
        return s % env

    env.dropbox       = os.path.expanduser("~/Dropbox")
    env.build_dir     = os.path.abspath("build")
    env.docs_dir     = os.path.abspath("docs")
    env.dist_dir      = os.path.join(env.dropbox, "dist", env.projectname, "%(projectname)s-%(package_version)s" % env)
    env.doc_package       = os.path.join(env.build_dir, versioned_file("doc"))
    env.templates_package = os.path.join(env.build_dir, versioned_file("templates", "zip"))
    env.static_package    = os.path.join(env.build_dir, versioned_file("static", "zip"))

    if not os.path.exists(env.build_dir):
        print red("creating build dir.")
        local("mkdir " + env.build_dir)

@task
def print_env():
    for key in "projectname package_version build_dir dist_dir version_file".split():
        print yellow(key), green(getattr(env, key))


# vim: set ft=python ts=4 sw=4 expandtab :
