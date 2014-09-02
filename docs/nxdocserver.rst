=================================
How to use the nxdocserver Script
=================================

:Date: |today|

Abstract
========

This is a quick overview on how to use the nxdocserver script.

Introduction
============

This script allows you to manage documentation meta data and files via a
commandline interface.

Commands
========

The following commands can be used::

    create_doc
    create_project
    delete_doc
    delete_project
    update_doc
    update_project

To receive more information on how to use the commands execute them with the
--help flag.

Configuration
=============

The script expects a configuration file in your home directory. This file must be
named `.nxdocserver` and match the following schema::

    [Login]
    user: XXXXXXXXX
    password: xxxxx

    [Docserver]
    url: http://docs.nexiles.com
    dropbox: /path/to/Dropbox/folder

.. caution:: Without this file or when options are missing in the file the script
             will fail with an Error.

.. vim: set ft=rst ts=4 sw=4 expandtab tw=78 :
