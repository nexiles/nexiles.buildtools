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

**nxdocserver create_doc --help** and this will show the Options
that are required and the Options which are not. ::

    $ nxdocserver create_doc --help
    Usage: nxdocserver create_doc [OPTIONS]
    Create a new documentation.
    Options:
    --project TEXT  ID of the parent project  [required]
    --title TEXT    Title of the documentation  [required]
    --version TEXT  Version of the documentation
    --zip PATH      Location of the zip file  [required]
    --icon PATH     Location of the icon file
    --help          Show this message and exit.


As mentioned above, there are several commands that can be applied to the
nxdocserver. When you want to use one of these commands, you have to say
in Terminal:

**nxdocserver create_project**. Some textwhich explains this here

Example::

    $ nxdocserver create_project --title test
    [localhost] local: mkdir -p /Users/jwycislok/develop/Trash/FakeBox/test

**nxdocserver create_doc**. This is a command to create a new documentation.
And when you want to see more informations or options about this command.

Example::

    $ nxdocserver create_doc --project test --title foo --zip foo.zip                                                                        
    [localhost] local: mkdir -p /Users/jwycislok/develop/Trash/FakeBox/test/foo-0-1.0/0.1.0
    [localhost] local: cp foo.zip /Users/jwycislok/develop/Trash/FakeBox/test/foo-0-1.0/0.1.0.zip
    [localhost] local: unzip /Users/jwycislok/develop/Trash/FakeBox/test/foo-0-1.0/0.1.0.zip
    Archive:  /Users/jwycislok/develop/Trash/FakeBox/test/foo-0-1.0/0.1.0.zip
     extracting: index.html


**nxdocserver update_doc** update a existing documentation, you have to say

Example::

  $ nxdocserver update_doc foo-0-1.0 --project test
nxdocserver update_doc has no output.
foo-0-1.0 is replaced by the title attribute in plone.



**nxdocserver update_project** update a existing documentation, you have to say

Example ::

  $ nxdocserver update_project test
nxdocserver update_project has no output.


**nxdocserver list_docs** list all documentation on the server.

Example ::

  $ nxdocserver list_docs
  nexiles-documentation-project                 released        Jan Müller           0.1             external   Sep 05, 2014 11:45 AM
  nexiles-documentation-project                 draft           Jan Müller           0.2.1           external   Sep 05, 2014 11:45 AM
  nexiles|gateway attributeservice (0.1)        released        Stefan Eletzhofer    0.1             external   Aug 14, 2014 02:31 PM
  nexiles|gateway attributeservice (0.1dev)     private         Stefan Eletzhofer    0.1dev          private    Aug 14, 2014 02:19 PM
  nexiles|gateway attributeservice (0.2dev)     draft           Stefan Eletzhofer    0.2dev          external   Aug 14, 2014 02:19 PM
  nexiles|gateway collectorservice (0.1)        released        Stefan Eletzhofer    0.1             external   Aug 14, 2014 02:31 PM
  nexiles|gateway collectorservice (0.1dev)     private         Stefan Eletzhofer    0.1dev          private    Aug 14, 2014 02:19 PM
  nexiles|gateway fileservice (0.1)             released        Stefan Eletzhofer    0.1             external   Aug 14, 2014 02:31 PM
  nexiles|gateway fileservice (0.1dev)          private         Stefan Eletzhofer    0.1dev          private    Aug 14, 2014 02:19 PM
  nexiles|gateway fileservice (0.2dev)          draft           Stefan Eletzhofer    0.2dev          external   Aug 14, 2014 02:29 PM
  nexiles|gateway numberservice (0.1)           private         Stefan Eletzhofer    0.1             private    Aug 14, 2014 02:19 PM
  nexiles|gateway numberservice (0.1dev)        private         Stefan Eletzhofer    0.1dev          private    Aug 14, 2014 02:19 PM
  nexiles|gateway numberservice (0.2)           released        Stefan Eletzhofer    0.2             external   Aug 14, 2014 02:29 PM
  nexiles|gateway numberservice (0.2dev)        private         Stefan Eletzhofer    0.2dev          private    Aug 14, 2014 02:19 PM
  nexiles|gateway numberservice (0.3dev)        draft           Stefan Eletzhofer    0.3dev          external   Aug 14, 2014 02:29 PM
  nexiles|gateway principalservice (0.1)        draft           Stefan Eletzhofer    0.1             external   Aug 14, 2014 02:29 PM
  nexiles|gateway principalservice (0.1dev)     private         Stefan Eletzhofer    0.1dev          private    Aug 14, 2014 02:19 PM
  nexiles|gateway query (0.1) service           private         Stefan Eletzhofer    0.1             private    Aug 14, 2014 02:19 PM
  nexiles|gateway query (0.1dev) service        private         Stefan Eletzhofer    0.1dev          private    Oct 14, 2014 10:50 AM
  nexiles|gateway query (0.2) service           released        Stefan Eletzhofer    0.2             external   Aug 14, 2014 02:28 PM
  nexiles|gateway query (0.2dev) service        private         Stefan Eletzhofer    0.2dev          private    Oct 14, 2014 10:50 AM
  nexiles|gateway reportservice (0.1)           released        Stefan Eletzhofer    0.1             external   Aug 14, 2014 02:29 PM
  nexiles|gateway reportservice (0.1dev)        private         Stefan Eletzhofer    0.1dev          private    Aug 14, 2014 02:19 PM
  nexiles|gateway reportservice (0.2dev)        draft           Stefan Eletzhofer    0.2dev          external   Aug 14, 2014 02:28 PM
  nexiles|gateway zipservice (0.1)              released        Stefan Eletzhofer    0.1             external   Aug 14, 2014 02:28 PM
  nexiles|gateway zipservice (0.1dev)           private         Stefan Eletzhofer    0.1dev          private    Aug 14, 2014 02:19 PM
  Gateway Installation Manual                   draft           Stefan Eletzhofer    1.4.7           internal   Oct 14, 2014 05:17 PM
  nexiles.buildtools                            draft           Stefan Eletzhofer    0.1             internal   Sep 11, 2014 01:52 PM
  siemens.tdsm                                  draft           Stefan Eletzhofer    0.1.0           internal   Sep 29, 2014 05:03 PM
  frenco.baselines                              private         Stefan Eletzhofer    0.1.0           private    Sep 16, 2014 11:32 AM
  siemens.saveas                                private         Ramon Bartl          0.1.0           private    Sep 17, 2014 01:16 PM
  macgregor.drawinglist                         draft           Stefan Eletzhofer    0.1.4           internal   Sep 22, 2014 06:20 PM
  macgregor                                     draft           Stefan Eletzhofer    0.1.0           internal   Sep 22, 2014 06:47 PM
  macgregor.drawinglist-0.1.5                   draft           Ramon Bartl          0.1.5           internal   Oct 09, 2014 03:51 PM
  cargotec.erp-0.4.5                            private         Ramon Bartl          0.4.5           private    Oct 09, 2014 04:07 PM
  nexiles|gateway query (0.3dev) service        draft           Stefan Eletzhofer    0.3dev          internal   Oct 14, 2014 10:50 AM
  nexiles gateway (1.4.7rc3) docs               draft           Sven Schmid          1.4.7           internal   Oct 14, 2014 05:18 PM
  hurz-0.1.0                                    private         Jan Börner           0.1.0           private    Nov 17, 2014 09:52 AM
  foo-0.1.0                                     private         Jan Börner           0.1.0           private    Nov 20, 2014 09:36 AM


**nxdocserver list_projects** list all projects on the server.

Example ::

  $ nxdocserver list_projects
  Project Title                            Project State   Project Creator      GitHub URL
  nexiles-documentation-project            released        Jan Müller           https://github.com/nexiles/nexiles-documentation-project
  Nexiles Gateway                          draft           None                 https://github.com/nexiles/nexiles.tools
  nexiles.gateway.attributeservice         released        Stefan Eletzhofer    https://github.com/nexiles/nexiles.gateway.attributeservice
  nexiles.gateway.collectorservice         released        Stefan Eletzhofer    https://github.com/nexiles/nexiles.gateway.collectorservice
  nexiles.gateway.fileservice              released        Stefan Eletzhofer    https://github.com/nexiles/nexiles.gateway.fileservice
  nexiles.gateway.numberservice            released        Stefan Eletzhofer    https://github.com/nexiles/nexiles.gateway.numberservice
  nexiles.gateway.principalservice         released        Stefan Eletzhofer    https://github.com/nexiles/nexiles.gateway.principalservice
  nexiles.gateway.query                    released        Stefan Eletzhofer    https://github.com/nexiles/nexiles.gateway.query
  nexiles.gateway.reportservice            released        Stefan Eletzhofer    https://github.com/nexiles/nexiles.gateway.reportservice
  nexiles.gateway.zipservice               released        Stefan Eletzhofer    https://github.com/nexiles/nexiles.gateway.zipservice
  nexiles.buildtools                       draft           Stefan Eletzhofer    https://github.com/nexiles/nexiles.buildtools
  siemens                                  draft           Stefan Eletzhofer    https://github.com/nexiles/siemens
  siemens.tdsm                             draft           Stefan Eletzhofer    https://github.com/nexiles/siemens.tdsm
  macgregor                                draft           Stefan Eletzhofer    https://github.com/nexiles/macgregor
  frenco.baselines                         private         Stefan Eletzhofer    https://github.com/nexiles/frenco.baselines
  siemens.saveas                           private         Ramon Bartl          https://github.com/nexiles/siemens.saveas
  macgregor.drawinglist                    draft           Stefan Eletzhofer    https://github.com/nexiles/macgregor.drawinglist
  cargotec.erp                             draft           Ramon Bartl          https://github.com/nexiles/cargotec.erp
  test3                                    private         Jan Börner           https://github.com/nexiles/nexiles.buildtools/milestones/nexiles-buildtools%200.1.0
  test                                     private         Jan Börner           https://github.com/nexiles/test


**nxdocserver delete_doc** delete documentation, you have to say

Example ::

  $ nxdocserver delete_doc foo-0-1.0 --project test
nxdocserver delete_doc has no output.
foo-0-1.0 is replaced by the title attribute in plone.

**nxdocserver delete_project** delete documentation, you have to say

Example ::

  $ nxdocserver delete_project test
nxdocserver delete_project has no output.


Examples
========
*This is an Example of a whole life cycle of a documentation*:
The first thing what you have to do is to beginn a project. For this project
you create a documentation. In this documentation, you write all the
informations about the project. Then you create another documentation.
If there are any changes, you need to update the documentation, so that it is up-to-stand.
Sometime the documentation and the whole project will be deleted.


.. vim: set ft=rst ts=4 sw=4 expandtab tw=78 :
