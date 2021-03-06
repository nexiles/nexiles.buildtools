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

Important
==========

**Only small letters are allowed by using the nxdocserver tools. When you use big letters, the backend of the nxdocserver get`s confused.**


Commands
========

The following commands can be used

    - create_doc
    - create_project
    - delete_doc
    - delete_project
    - list_doc
    - list_projects
    - update_doc
    - update_project

For every command there is the detail for the documentation as well as for the
project. 

+-------------------------------+-----------------------------+------------------------------+---------------------------------+
| create_doc & create_project   | delete_doc & delete_project | list_docs & list_projects    | update_doc & update_project     |
+===============================+=============================+==============================+=================================+
| create a new documentation or | delete a documentation      | list all documentation or    | update a existing documentation |
| a new project                 | or a project                | all projects on the server   | or a exisiting create_project   |
+-------------------------------+-----------------------------+------------------------------+---------------------------------+


To receive more information on how to use the commands, execute every command with the
--help flag. Options taged with **[required]** are required for the certain command::

  $ nxdocserver COMMAND_NAMEE --help
    Information about the command.

    Options:
      --projInformation about the commandparent project
      --title TEXT    Title of the project  [required]
      --github TEXT   GitHub URL of the project
      --help          Show this message and exit.

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

To install the **nxdcoserver** command you've to follow 3 steps:
    
    - Clone the git repo

    - Go to the project home directory

    - Create a virtualenv and install the requirements

    - Run the python install script

    ::

    $ git clone git@github.com:nexiles/nexiles.buildtools.git
    $ cd $PROJECT_HOME
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


To get informations about a certain command typ **--help**.

**nxdocserver create_project**
------------------------------

To create a project you've to use the **create_project** command like in the
Example.

Example::

    $ nxdocserver create_project --title test
    [localhost] local: mkdir -p /Users/jwycislok/develop/Trash/FakeBox/test

**nxdocserver create_doc** 
--------------------------

This is a command to create a new documentation.
And when you want to see more informations or options about this command.

Example::

    $ nxdocserver create_doc --project test --title foo --zip foo.zip                                                                        
    [localhost] local: mkdir -p /Users/jwycislok/develop/Trash/FakeBox/test/foo-0-1.0/0.1.0
    [localhost] local: cp foo.zip /Users/jwycislok/develop/Trash/FakeBox/test/foo-0-1.0/0.1.0.zip
    [localhost] local: unzip /Users/jwycislok/develop/Trash/FakeBox/test/foo-0-1.0/0.1.0.zip
    Archive:  /Users/jwycislok/develop/Trash/FakeBox/test/foo-0-1.0/0.1.0.zip
     extracting: index.html


**nxdocserver update_doc**
--------------------------

To update a documentation you've to use the **update_doc** command like in the
Example.

.. caution:: nxdocserver update_doc has no output. foo-0-1.0 is replaced by the title attribute in plone.

Example::

  $ nxdocserver update_doc foo-0-1.0 --project test

**nxdocserver update_project**
------------------------------


This commands updates a existing project.

Example::

  $ nxdocserver update_project test

.. caution:: nxdocserver update_project has no output.


**nxdocserver list_docs**
-------------------------

This command lists all documentation on the server.

Example::

  $ nxdocserver list_docs
  nexiles-documentation-project                 released        Jan Müller           0.1             external   Sep 05, 2014 11:45 AM
  nexiles-documentation-project                 draft           Jan Müller           0.2.1           external   Sep 05, 2014 11:45 AM
  nexiles|gateway attributeservice (0.1)        released        Stefan Eletzhofer    0.1             external   Aug 14, 2014 02:31 PM
  nexiles|gateway attributeservice (0.1dev)     private         Stefan Eletzhofer    0.1dev          private    Aug 14, 2014 02:19 PM
  nexiles|gateway attributeservice (0.2dev)     draft           Stefan Eletzhofer    0.2dev          external   Aug 14, 2014 02:19 PM
  nexiles|gateway collectorservice (0.1)        released        Stefan Eletzhofer    0.1             external   Aug 14, 2014 02:31 PM
  nexiles|gateway collectorservice (0.1dev)     private         Stefan Eletzhofer    0.1dev          private    Aug 14, 2014 
  .............


**nxdocserver list_projects** 
-----------------------------

This command lists all projects on the server.

Example::

  $ nxdocserver list_projects
  Project Title                            Project State   Project Creator      GitHub URL
  nexiles-documentation-project            released        Jan Müller           https://github.com/nexiles/nexiles-documentation-project
  Nexiles Gateway                          draft           None                 https://github.com/nexiles/nexiles.tools
  nexiles.gateway.attributeservice         released        Stefan Eletzhofer    https://github.com/nexiles/nexiles.gateway.attributeservice
  nexiles.gateway.collectorservice         released        Stefan Eletzhofer    https://github.com/nexiles/nexiles.gateway.collectorservice
  nexiles.gateway.fileservice              released        Stefan Eletzhofer    https://github.com/nexiles/nexiles.gateway.fileservice                                  private         Jan Börner           https://github.com/nexiles/test 
  ..............


**nxdocserver delete_doc** 
--------------------------

This command deletes a documentation.

.. caution:: nxdocserver delete_doc has no output. foo-0-1.0 is replaced by the title attribute in plone.

Example::

  $ nxdocserver delete_doc foo-0-1.0 --project test


**nxdocserver delete_project** 
------------------------------


This commands deletes a documentation.
.. caution::  nxdocserver delete_project has no output.

Example::

  $ nxdocserver delete_project test



Examples
========

To see how it works, we create a little project. 
First we have to create our new project and give it a name. Our project has the name "Example"
::

  $ nxdocserver create_project --title Example

After we created the project "Example" we have to write a documentation about it. So we have to create a 
documentation.
::

  $ nxdocserver create_doc --project Example --title foo --zip foo.zip

Maybe we need more documentation for this project, so we have to do the same as above.

Now we should update the documentation because a lot has changed in the documentation and that we are up-to-date
we must do:
::

  $ nxdocserver update_doc foo-0-1.0 --project Example

Because the documentation has changed, the whole project should be up to date, we also update the entire project.
::

  $ nxdocserver update_project Example

Sometime the project is finished and we don´t need the documentations, we will delete the documentations
::

  $ nxdocserver delete_doc foo.0-1.0 --project Example

We don´t need a project Without some documentations or contents, so now we can delete the whole project.
::

  $ nxdocserver delete_project Example

Now the whole project no longer exist.

.. vim: set ft=rst ts=4 sw=4 expandtab tw=78 :
