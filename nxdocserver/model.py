# -*- coding: utf-8 -*-
import logging, click

class TypedResource(object):
    """ Wrapper for API results
    """

    def __init__(self, data):
        self.logger = logging.getLogger("typed_resource.%s" % type)
        self.data = data

    def __getitem__(self, key):
        if not key in self.data.keys():
            raise KeyError(key)
        return self.data[key]

class Folder(TypedResource):
    type = "folders"

class Docmeta(TypedResource):
    type = "docmetas"

class Project(TypedResource):
    type = "projects"

    def __iter__(self):
        return iter(self.data["docs"])

    def __contains__(self, title):
        for item in self:
            if item["title"] == title:
                return True
        raise KeyError(title)

    def getByUid(self, uid):
        for item in self:
            if item["uid"] == uid:
                return Docmeta(item)
        raise KeyError(uid)

    def getById(self, name):
        """ Return a docmeta or throw a click.ClickException
        """
        docs = filter(lambda item: item["id"] == name, self)
        if not docs:
            raise click.ClickException("Documentation not found. Aborting")

        return Docmeta(docs[0])
