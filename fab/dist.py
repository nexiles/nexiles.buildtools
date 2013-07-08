import os
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

from nxfab import eggs, egg_for_customer

def dist_package(package):
    if not os.path.exists(env.dist_dir):
        print red("creating dist dir: %s" % env.dist_dir)
        local("mkdir -p '%s'" % env.dist_dir )
    local("cp %s %s" % (package, env.dist_dir))

@task
def dist_templates():
    """dist_templates -- copy template package to dist"""
    dist_package(env.templates_package)
    print green("copied %(templates_package)s to %(dist_dir)s" % env)

@task
def dist_static():
    """dist_static -- dist static file package"""
    dist_package(env.static_package)
    print green("copied %(static_package)s to %(dist_dir)s" % env)

@task
def dist_docs():
    """dist_docs -- dist docs package"""
    dist_package(env.doc_package)
    print green("copied %(doc_package)s to %(dist_dir)s" % env)

@task
def dist_eggs():
    # copy stuff
    for package, egg in eggs():
        local("cp src/%s/dist/%s %s" % (package, egg_for_customer(egg), env.dist_dir))
        print yellow("disted %s" % egg_for_customer(egg))

# vim: set ft=python ts=4 sw=4 expandtab :
