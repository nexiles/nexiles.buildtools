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

# vim: set ft=python ts=4 sw=4 expandtab :
