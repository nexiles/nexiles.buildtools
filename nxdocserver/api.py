import os
import json
import logging
import requests
from model import *

class API(object): # <clazz extends TypedResource>
    """ A generic API class
        Returns objects of type clazz
    """
    def __init__(self, clazz, base_url, api, username, password):
        self.clazz = clazz
        self.base_url = base_url
        self.api = api
        self.username = username
        self.password = password
        self.session = requests.Session()

        self.logger = logging.getLogger("api.%s" % self.api)

    def _api_uri(self, api):
        return "@@API/{0}/api/1.0".format(api)

    def make_url(self, *args):
        uri = self._api_uri(self.api)
        return os.path.join(self.base_url, uri, *args)

    def get(self, *args):
        url = self.make_url(self.clazz.type, *args)
        self.logger.debug("GET (%s): %s", self.clazz.type, url)
        ret = self.session.get(url, auth=(self.username, self.password)).json()
        if "error" in ret:
            raise RuntimeError(ret["error"])

        return ret

    def post(self, *args, **kw):
        headers = {'content-type': 'application/json'}
        url = self.make_url(self.clazz.type, *args)
        self.logger.debug("POST (%s): %s", self.clazz.type, url)
        if kw:
            self.logger.debug("POST DATA: %r", kw)
            ret = self.session.post(url, auth=(self.username, self.password), data=json.dumps(kw), headers=headers).json()
        else:
            ret = self.session.post(url, auth=(self.username, self.password), headers=headers).json()

        if "error" in ret:
            raise RuntimeError(ret["error"])

        return ret

    def find(self, key, value):
        ret = self.get()
        for item in ret["items"]:
            if item[key] == value:
                return self.clazz(item)

    def list(self):
        ret = self.get()
        return map(lambda item: self.clazz(item), ret["items"])

    def create(self, parent_uid, **kw):
        self.logger.debug("create: parent=%s, %r", parent_uid, kw)
        ret = self.post("create", parent_uid, **kw)
        self.logger.debug("created: => %r", ret)
        return self.clazz(ret["items"][0])

    def update(self, uid, **kw):
        self.logger.debug("update: uid=%s, %r", uid, kw)
        ret = self.post("update", uid, **kw)
        self.logger.debug("updated: => %r", ret)
        return self.clazz(ret["items"][0])

    def delete(self, uid):
        self.logger.debug("delete: uid=%s", uid)
        ret = self.post("delete", uid)
        self.logger.debug("deleted: => %r", ret)
        return ret

class FolderAPI(API): # extends API<Folder>

    def __init__(self, base_url, username, password):
        super(self.__class__, self).__init__(Folder, base_url, "plone", username, password)

class DocmetaAPI(API): # extends API<Docmeta>

    def __init__(self, base_url, username, password):
        super(self.__class__, self).__init__(Docmeta, base_url, "docs", username, password)

class ProjectAPI(API): # extends API<Project>

    def __init__(self, base_url, username, password):
        super(self.__class__, self).__init__(Project, base_url, "docs", username, password)
