# -*- coding: utf-8 -*-

import os
import click
import string
import logging

class TypedResource(object):
    """ Wrapper for API results
    """

    def __init__(self, data):
        self.logger = logging.getLogger("typed_resource.%s" % type)
        self.data = data

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        return self.data.__setitem__(key, value)

    def update(self, data):
        return self.data.update(data)

    def delete(self):
        return self.__class__.api.delete(self["uid"])

    def format(self, fmt):
        return ResourceFormatter().format(fmt, self)

class ResourceFormatter(string.Formatter):
    def get_field(self, key, args, kwargs):
        value = None
        context = args[0]
        for subkey in key.split("."):
            context = value = context[subkey]
        return (value, key)

class Folder(TypedResource):
    type = "folders"

class Docmeta(TypedResource):
    type = "docmetas"

    def save(self):
        if "uid" in self.data.keys():
            Docmeta.api.update(self["uid"], title=self["title"], version=self["version"], doc_icon=self["doc_icon"])
            return

        version = self["version"]
        title = self["title"]

        versioned_title = "%s-%s" % (title, version)

        parent = Project.api.find("id", self.data["parent_id"])
        if not parent:
            raise click.ClickException("Parent project not found. Aborting")

        # Check for duplicates
        for doc in parent:
            if doc["title"] == title and doc["version"] == version:
                raise click.ClickException("Documentation already exists. Aborting")

        # create meta data
        data = Docmeta.api.create(parent["uid"], title=versioned_title, version=self["version"])

        if self["icon"]:
            # add the icon to the docmeta
            data = Docmeta.api.update(data["uid"], doc_icon=os.path.join(self["parent"], data["id"], "icon.png"))

        self.data = data

class Project(TypedResource):
    type = "projects"

    def __iter__(self):
        return iter(self.data["docs"])

    def __contains__(self, title):
        for item in self:
            if item["title"] == title:
                return True
        raise KeyError(title)

    def save(self):
        if "uid" in self.data.keys():
            Project.api.update(self["uid"], title=self["title"], github=self["github"])
            return

        # Check for duplicates
        if Project.api.find("title", self["title"]):
            raise click.ClickException("A Project with this title already exists")

        if "parent_id" in self.data.keys() and self["parent_id"]:
            # nested project
            parent = Project.api.find("id", self["parent_id"])
        else:
            # add to documentation folder as default
            parent = Folder.api.find("title", "Documentation")

        if not parent:
            raise click.ClickException("Parent not found. Aborting")

        # create meta data
        self.data = Project.api.create(parent["uid"], title=self["title"], github=self["github"])

    def getByUid(self, uid):
        for item in self:
            if item["uid"] == uid:
                return Docmeta(item)
        raise KeyError(uid)

    def getById(self, name):
        """ Return a docmeta or None
        """
        docs = filter(lambda item: item["id"] == name, self)
        if not docs:
            return None

        return Docmeta(docs[0])
