# -*- coding: utf-8 -*-
from api import API
import logging, click

class TypedResource(object):
    def __init__(self, api, type):
        self.type = type
        self.api = api
        self.logger = logging.getLogger("typed_resource.%s" % type)

    def get(self, *args):
        return self.api.get(self.type, *args)

    def post(self, *args, **kw):
        return self.api.post(self.type, *args, **kw)

    def find(self, key, value):
        ret = self.get()
        for item in ret["items"]:
            if item[key] == value:
                return item

    def list(self):
        ret = self.get()
        return ret["items"]

    def __getitem__(self, uid):
        for item in self:
            if item["uid"] == uid:
                return item
        raise KeyError(uid)

    def __iter__(self):
        return iter(self.list())

    def __contains__(self, title):
        for p in self:
            if p["title"] == title:
                return True
        raise KeyError(title)

    def create(self, parent_uid, **kw):
        self.logger.debug("create: parent=%s, %r", parent_uid, kw)
        ret = self.post("create", parent_uid, **kw)
        self.logger.debug("created: => %r", ret)
        return ret["items"][0]

    def update(self, uid, **kw):
        self.logger.debug("update: uid=%s, %r", uid, kw)
        ret = self.post("update", uid, **kw)
        self.logger.debug("updated: => %r", ret)
        return ret["items"][0]

    def delete(self, uid):
        self.logger.debug("delete: uid=%s", uid)
        ret = self.post("delete", uid)
        self.logger.debug("deleted: => %r", ret)
        return ret


class PloneFolders(TypedResource):
    def __init__(self, api):
        TypedResource.__init__(self, api, "folders")

class Docmetas(TypedResource):
    def __init__(self, api):
        TypedResource.__init__(self, api, "docmetas")

class Projects(TypedResource):
    def __init__(self, api):
        TypedResource.__init__(self, api, "projects")

    def find_docmeta(self, name, project):
        """ Return a docmeta or throw a click.ClickException
        """
        project = self.find("id", project)
        if not project:
            raise click.ClickException("Parent project not found. Aborting")

        docs = filter(lambda item: item["id"] == name, project["docs"])
        if not docs:
            raise click.ClickException("Documentation not found. Aborting")

        return docs[0]
