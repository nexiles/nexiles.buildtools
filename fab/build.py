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

def zip_package(package, dir, root):
    with lcd(dir):
        local("zip -r %(package)s %(root)s" % locals())

@task
def build_templates(dir="src"):
    """build_templates -- package the templates"""
    zip_package(env.templates_package, dir, "templates")

@task
def build_static(dir="src"):
    """build_static -- package static files"""
    zip_package(env.static_package, dir, "static")

# vim: set ft=python ts=4 sw=4 expandtab :
