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
