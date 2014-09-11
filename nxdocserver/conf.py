# -*- coding: utf-8 -*-
#
# File: conf.py
#
# Copyright (c) nexiles GmbH
#
__author__    = """Stefan Eletzhofer <se@nexiles.de>"""
__docformat__ = 'plaintext'
__revision__  = "$Revision: $"
__version__   = '$Revision: $'[11:-2]

import os
import sys
import ConfigParser

class ConfigError(Exception):
    pass


class Configuration(object):
    CONFIG_FILE_NAME = ".nxdocserver"

    def __init__(self):
        self.config = self.read()

    def read(self):
        config_file_path = os.path.expanduser("~/%s" % self.CONFIG_FILE_NAME)
        if not os.path.exists(config_file_path):
            raise ConfigError("Config file not found: %s" % config_file_path)

        config = ConfigParser.SafeConfigParser()
        config.read(os.path.expanduser("~/.nxdocserver"))

        return config

    @property
    def docserver_url(self):
        return self.config.get("Docserver", "url")

    @property
    def docserver_dropbox(self):
        return self.config.get("Docserver", "dropbox")

    @property
    def login_username(self):
        return self.config.get("Login", "user")

    @property
    def login_password(self):
        return self.config.get("Login", "password")


def get_configuration():
    return Configuration()

# vim: set ft=python ts=4 sw=4 expandtab :
