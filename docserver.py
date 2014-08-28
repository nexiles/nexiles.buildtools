# -*- coding: utf-8 -*-
import os
import json
import logging
import requests


class API(object):
    def __init__(self, base_url, api, username, password):
        self.api = api
        self.base_url = base_url
        self.username = username
        self.password = password
        self.session = requests.Session()

        self.logger = logging.getLogger("api.%s" % api)

    def _api_uri(self, api):
        return "@@API/{0}/api/1.0".format(api)

    def make_url(self, *args):
        uri = self._api_uri(self.api)
        return os.path.join(self.base_url, uri, *args)

    def get(self, action, *args):
        url = self.make_url(action, *args)
        self.logger.debug("GET (%s): %s", action, url)
        ret = self.session.get(url, auth=(self.username, self.password)).json()
        if "error" in ret:
            raise RuntimeError(ret["error"])

        return ret

    def post(self, action, *args, **kw):
        headers = {'content-type': 'application/json'}
        url = self.make_url(action, *args)
        self.logger.debug("POST (%s): %s", action, url)
        if kw:
            self.logger.debug("POST DATA: %r", kw)
            ret = self.session.post(url, auth=(self.username, self.password), data=json.dumps(kw), headers=headers).json()
        else:
            ret = self.session.post(url, auth=(self.username, self.password), headers=headers).json()

        if "error" in ret:
            raise RuntimeError(ret["error"])

        return ret

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


def test():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)-7s] [line %(lineno)d] %(name)s: %(message)s")

    DOCSERVER_URL = "http://docs.nexiles.com"
    username = "seletz"
    password = "12345"

    plone_api = API(DOCSERVER_URL, "plone", username, password)
    docs_api  = API(DOCSERVER_URL, "docs", username, password)

    docs_api.logger.setLevel(logging.DEBUG)

    folders   = PloneFolders(plone_api)

    projects  = Projects(docs_api)
    projects.logger.setLevel(logging.DEBUG)

    docmetas  = Docmetas(docs_api)
    docmetas.logger.setLevel(logging.DEBUG)

    # list all projects
    for p in projects:
        print "{title} {state} {github}".format(**p)

    print "Nexiles Gateway" in projects

    # TEST PROJECTS API
    # -----------------------------

    # create a project
    parent_uid = folders.find("title", "Documentation")["uid"]
    p = projects.create(parent_uid, title="Test Project", github="https://github.com/nexiles/nexiles.plone.docs")

    # update
    p = projects.update(p["uid"], github="http://google.de")
    assert p["github"] == "http://google.de"

    # TEST DOCMETAS
    # -----------------------------

    # create a project
    d = docmetas.create(
        p["uid"],
        title="Test Doc",
        version="0.0.1",
        icon=None)

    # update
    d = docmetas.update(d["uid"], icon="foo.jpg")
    assert d["icon"].endswith("foo.jpg")

    # CLEANUP
    # -------

    # delete docmeta
    docmetas.delete(d["uid"])

    # delete project
    projects.delete(p["uid"])

if __name__ == '__main__':
    test()

# vim: set ft=python ts=4 sw=4 expandtab :

