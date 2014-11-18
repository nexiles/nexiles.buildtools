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
    list_doc
    list_projects
    update_doc
    update_project

For every command there is the detail for the documentation as well as for the
project. 

+-------------------------------+-----------------------------+------------------------------+---------------------------------+
| create_doc & create_project   | delete_doc & delete_project | list_docs & list_projects    | update_doc & update_project     |
+===============================+=============================+==============================+=================================+
| create a new documentation or | delete a documentation      | list all documentation or    | update a existing documentation |
| a new project                 | or a project                | all projects on the server   | or a exisiting create_project   |
+-------------------------------+-----------------------------+------------------------------+---------------------------------+


To receive more information on how to use the commands execute them with the
--help flag. 

For example::

    nxdocserver create_doc --help

Configuration
=============

The script expects a configuration file in your home directory. This file must be
named **.nxdocserver** and match the following schema::

    [Login]
    user: XXXXXXXXX
    password: xxxxx

    [Docserver]
    url: http://docs.nexiles.com
    dropbox: /path/to/Dropbox/folder

.. caution:: Without this file or when options are missing in the file the script
             will fail with an Error.


Installation
============

::

$ cd $project
$ mkvirtualenv -a $(pwd) -r requirements.txt nexiles.buildtools
$ python setup.py install




Command line usage
==================
As mentioned above, there are several commands that can be applied to the
nxdocserver. When you want to use one of these commands, you have to say
in Terminal:

**nxdocserver create_doc**. This is a command to create a new documentation.
And when you want to see more informations or options about this command
you can say:

**nxdocserver create_doc --help** and this will show the Options
that are required and the Options which are not.


Examples
========
*This is an Example of a whole life cycle of a documentation*:
The first thing what you have to do is to beginn a project. For this project
you create a documentation. In this documentation, you write all the
informations about the project. Then you create another documentation.
If there are any changes, you need to update the documentation, so that it is up-to-stand.
Sometime the documentation and the whole project will be deleted.


.. vim: set ft=rst ts=4 sw=4 expandtab tw=78 :
