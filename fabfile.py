# -*- coding: utf-8 -*-

# copyright (c) 2013 nexiles GmbH

import os
import sys

from fabric.api import env

__version__ = "0.1"
__date__ = "2013-04-23"
__build__ = 0

sys.path.append(os.path.expanduser("%s/fab" % os.getcwd()))

env.version_file = os.path.abspath("%s/fabfile.py" % os.getcwd())
env.projectname = "nexiles.buildtools"

from nxfab import setup_version, setup_env
setup_version()
setup_env()

from docs import build_docs, package_docs
from nxdocserver.tasks import publish_docs

# vim: set ft=python ts=4 sw=4 expandtab :
