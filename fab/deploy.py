import os
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

from nxfab import eggs, egg_for_customer
from manifest import make_manifest_file

__all__ = ["deploy_eggs"]

@task
def deploy_eggs():
    """deploy eggs to server"""
    print "deploying version: " + yellow(env.package_version)

    print green("deploying code packages ...")
    dest = "%(WT_HOME)s/codebase/WEB-INF" % os.environ
    for package, egg in eggs():
        local("cp src/%s/dist/%s %s/lib-python/%s" % (package, egg_for_customer(egg), dest, egg))
        print yellow("deployed %s -> %s" % (egg_for_customer(egg), egg))

    print green("done.")


# vim: set ft=python ts=4 sw=4 expandtab :
