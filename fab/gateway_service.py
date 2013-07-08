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


sys.path.append(os.path.expanduser("~/develop/nexiles/nexiles.buildtools/fab"))

# project setup
from nxfab import setup_version
from nxfab import setup_env
from nxfab import print_env
from nxfab import eggs

# version tasks
from version import bump_version
from version import version
from version import get_version
from version import version_string

# documentation handling
from docs import build_docs
from docs import publish_docs
from docs import package_docs

# build tasks
from build import build_templates
from build import build_static
from build import build_eggs

# deploy tasks
from deploy import deploy_eggs

# dist tasks
from dist import dist_package
#from dist import dist_static
#from dist import dist_templates
from dist import dist_docs
from dist import dist_eggs

# gateway specific tasks
from gateway import reload


# ENV SETUP
# ------------------------------------------------------------------------------

# project name
# ------------
env.projectname = "nexiles.gateway.attributeservice"
env.projectname_docs = "nexiles.gateway.services/attributeservice"

# list of packages this fabfile builds
# ------------------------------------
env.packages = "nexiles.gateway.attributeservice".split()

# the file which is updated on bump_version
# -----------------------------------------
env.version_file = os.path.abspath("src/nexiles.gateway.attributeservice/nexiles/gateway/attributeservice/version.py")

# license file related configuration
# --------------------------------
env.license_file = os.path.abspath("src/nexiles.gateway.attributeservice/nexiles/gateway/attributeservice/license.py")
env.customer     = "nexiles"  # standard internal customer
env.package_uuid = "urn:uuid:a9146336-4530-4585-a470-f1d23bc59c9b"
env.license_tpl  = """# -*- coding: utf-8 -*-
LICENSE = {
        "customer_id": "%(customer)s",
        "key":         "%(package_uuid)s"
}
"""

setup_version()
setup_env()

# overwrite std dist dir
# ----------------------
env.dist_dir = os.path.join(env.dropbox, "dist", "nexiles.gateway.services", "attributeservice", "%(projectname)s-%(package_version)s" % env)

################################################################################
# BUILDING
################################################################################

@task
def build(customer=None):
    """Deploy nexiles.gateway.attributeservice to server"""
    if customer:
        env.customer = customer

    print "building version: " + yellow(env.package_version)
    print "for customer    : " + red(env.customer)

    build_eggs()
    build_docs()
    package_docs()

    print "built version   : " + green(version_string())
    print "for customer    : " + red(env.customer)

################################################################################
# DEVELOP
################################################################################

@task
def deploy(version=None, customer=None):
    """deploy nexiles.gateway.attributeservice jar and web app to server"""
    if customer:
        env.customer = customer
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
        env.customer = customer

    setup_version(ask=True)
    print "Creating dist packages for version: " + yellow(env.package_version)

    dist_docs()
    publish_docs()
    dist_eggs()

    with file("%(dist_dir)s/attributeservice-windows.pth" % env, "w") as all_pth:
        for package, egg in eggs():
            print >>all_pth, ".\\%s" % egg

    with file("%(dist_dir)s/attributeservice-unix.pth" % env, "w") as all_pth:
        for package, egg in eggs():
            print >>all_pth, "./%s" % egg

    with file("%(dist_dir)s/attributeservice-site.xconf" % env, "w") as xconf:
        print >>xconf, """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Configuration SYSTEM "xconf.dtd">
<Configuration xmlns:xlink="http://www.w3.org/1999/xlink">
    <Property name="nexiles.gateway.plugins" overridable="true" targetFile="codebase/wt.properties" value="nexiles.gateway.attributeservice"/>
</Configuration>
"""


    print
    print
    print "version      : ", red(env.package_version)
    print "code packages: ", red(" ".join([egg for package, egg in eggs()]))
    print "doc  packages: ", red(env.doc_package)
    print "dist dir     : ", red(env.dist_dir)



# vim: set ft=python ts=4 sw=4 tw=80 expandtab :

