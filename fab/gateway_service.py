import os
import sys
import json

import datetime
import zipfile
from hashlib import sha256

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


# project setup
from nxfab import setup_version
from nxfab import setup_env
from nxfab import print_env
from nxfab import eggs, egg_for_customer

# version tasks
from version import bump_version
from version import version
from version import get_version
from version import version_string

# documentation handling
from docs import build_docs
from nxdocserver.tasks import publish_docs
from docs import package_docs

# build tasks
from build import build_templates
from build import build_static
from build import build_eggs

# deploy tasks
from deploy import deploy_eggs

# dist tasks
from dist import dist_package
from dist import dist_docs
from dist import dist_eggs

# gateway specific tasks
from gateway import reload

# license file related configuration
# --------------------------------
env.customer_list = "nexiles settr cargotec rotator mtc schaeffler frenco"
env.license_tpl   = """# -*- coding: utf-8 -*-
LICENSE = {
        "customer_id": "%(customer)s",
        "key":         "%(package_uuid)s"
}
"""


################################################################################
# BUILDING
################################################################################

@task
def build_pth():
    """build a suitable pth file for windows and unix."""
    env.service_name = env.projectname.split(".")[-1]
    with file("%(build_dir)s/%(service_name)s-windows.pth" % env, "w") as all_pth:
        for package, egg in eggs():
            print >>all_pth, ".\\%s" % egg

    with file("%(build_dir)s/%(service_name)s-unix.pth" % env, "w") as all_pth:
        for package, egg in eggs():
            print >>all_pth, "./%s" % egg

@task
def build(customer=None):
    """Deploy nexiles gateway service to server"""
    if customer:
        customer_list = [customer]
    else:
        customer_list = env.customer_list.split()

    assert "WT_HOME" in os.environ, "Please set WT_HOME!"
    assert "PYTHONUSERBASE" in os.environ, "Please set PYTHONUSERBASE!"

    for customer in customer_list:
        env.customer = customer
        print "building version: " + yellow(env.package_version)
        print "for customer    : " + red(env.customer)
        build_eggs()

    build_pth()
    build_docs()
    package_docs()

    print "built version   : " + green(version_string())
    print "for customer    : " + red(customer_list)

################################################################################
# DEVELOP
################################################################################

@task
def deploy(version=None, customer=None):
    """deploy nexiles gateway service jar and web app to server"""
    if customer:
        env.customer = customer

    if "customer" not in env or env.customer is None:
        raise RuntimeError("no customer specified and env.customer not set.")

    print "deploying version : " + yellow(env.package_version)
    print "for customer      : " + red(env.customer)

    deploy_eggs()

    print "deployed version  : " + green(version_string())
    print "for customer      : " + red(env.customer)

@task
def update():
    """build, deploy, reload"""
    bump_version()
    build()
    deploy()
    reload(path="services/attributes/version")
    version()

################################################################################
# DIST
################################################################################


@task
def dist(version=None, customer=None):
    """create a dist package on the nexiles dist server"""
    if customer:
        customer_list = [customer]
    else:
        customer_list = env.customer_list.split()

    setup_version(ask=True)
    print "Creating dist packages for version: " + yellow(env.package_version)

    dist_docs()

    print "dist for "
    for customer in customer_list:
        env.customer = customer
        print red(env.customer), " "
        dist_eggs()
    print "done."

    if "additional_packages" in env:
        for p in env.additional_packages:
            print red("deploying additional package: " + p)
            dist_package(p, versionize=True)

    env.service_name = env.projectname.split(".")[-1]
    dist_package("%(build_dir)s/%(service_name)s-windows.pth" % env)
    dist_package("%(build_dir)s/%(service_name)s-unix.pth" % env)

    with file("%(dist_dir)s/%(service_name)ssite.xconf" % env, "w") as xconf:
        print >>xconf, """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Configuration SYSTEM "xconf.dtd">
<Configuration xmlns:xlink="http://www.w3.org/1999/xlink">
    <Property name="nexiles.gateway.plugins" overridable="true" targetFile="codebase/wt.properties" value="%(projectname)s"/>
</Configuration>
""" % env

    print
    print
    print "customers dist'd : ", red(customer_list)
    print "version          : ", red(env.package_version)
    print "code packages    : ", red(" ".join([egg_for_customer(egg) for package, egg in eggs()]))
    print "additional pkgs  : ", red(" ".join(env.get("additional_packages", [])))
    print "doc  packages    : ", red(env.doc_package)
    print "dist dir         : ", red(env.dist_dir)


# vim: set ft=python ts=4 sw=4 tw=80 expandtab :

