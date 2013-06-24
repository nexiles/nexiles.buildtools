import os
import re
import datetime
import fileinput

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

__all__ = ["version_string", "bump_version", "version"]

def write_version_info():
    """ updates the build and date of the version module
    """
    f = env.version_file
    if not os.path.exists(f):
        raise RuntimeError("File '%s' does not exist." % f)

    for line in fileinput.input(f, inplace=1):
        if re.findall("__build__.*=", line):
            build = int(line.split("=")[1])
            line = "__build__ = %d" % (build + 1)
        elif re.findall("__date__.*=", line):
            now = datetime.datetime.now().strftime("%Y-%m-%d")
            line = "__date__ = '%s'" % now
        print line.strip("\n")

def get_version():
    f = env.version_file
    out = {}
    lines = file(f).readlines()
    for l in lines:
        if "=" in l and l.split("=")[0].strip() in ("__build__", "__date__", "__version__"):
            name, value = l.split("=")
            name = name.strip(" _\n\r")
            value = value.strip(' "\'\n\r')
            out[name] = value
    return out

def version_string(version=None):
    if not version:
        version = get_version()
    return "version %(version)s build %(build)s date %(date)s" % (version)

@task
def bump_version():
    """Bump up the version number"""
    print yellow("bumping version ...")
    write_version_info()
    print red("adding file '%s' to next commit." % env.version_file)
    local("git add " + env.version_file)
    print "updated version: ", version_string()

@task
def version():
    """Print current version of nexiles.gateway.attributeservice package."""
    print green(version_string())

# vim: set ft=python ts=4 sw=4 expandtab :
