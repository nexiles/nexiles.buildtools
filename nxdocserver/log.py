# -*- coding: utf-8 -*-
#
# File: log.py
#
# Copyright (c) nexiles GmbH

__author__    = """Stefan Eletzhofer <se@nexiles.de>"""
__docformat__ = 'plaintext'
__revision__  = "$Revision: $"
__version__   = '$Revision: $'[11:-2]


import os
import sys
import logging

logger = logging.getLogger("nxdocserver")

def setup_logging(level=logging.DEBUG):
    logging.basicConfig(level=level, format="%(asctime)s [%(levelname)-7s] [line %(lineno)d] %(name)s: %(message)s")




# vim: set ft=python ts=4 sw=4 expandtab :
