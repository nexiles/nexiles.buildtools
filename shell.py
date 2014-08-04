# -*- coding: utf-8 -*-
import os
import json
import glob
import requests

from fabric.api import env, task, lcd, local, execute, settings, hide
from fabric.colors import green, yellow, red

DOCSERVER_URL = "http://docs.nexiles.com"
username = "seletz"
password = "12345"

docserver_dist = os.path.expanduser("~/Dropbox/docserver/docs")
dist_folder    = os.path.expanduser("~/Dropbox/dist")


def make_api_url(action, api="docs"):
    DOC_API_URI   = "@@API/{0}/api/1.0".format(api)
    if action:
        url = os.path.join(DOCSERVER_URL, DOC_API_URI, action)
    else:
        url = os.path.join(DOCSERVER_URL, DOC_API_URI)
    return url

def post(data, action):
    headers = {'content-type': 'application/json'}
    url = make_api_url(action, api="docs")
    print "POST (" + action + "): " + url
    ret = requests.post(url, auth=(username, password), data=json.dumps(data), headers=headers).json()
    if "error" in ret:
        raise RuntimeError(ret["error"])

    return ret

def create(parent, **kw):
    return post(kw, "create/%s" % parent)

def update(uid, **kw):
    return post(kw, "update/%s" % uid)

def find(api, action, key, value):
    url = make_api_url(action, api=api)
    if key == "url":
        value = os.path.join(DOCSERVER_URL, value)
    ret = requests.get(url, auth=(username, password)).json()
    for item in ret["items"]:
        if item[key] == value:
            return item

def find_parent_folder(path):
    return find("plone", "folders", "url", path)

def find_docmeta(title):
    return find("docs", None, "name", title)

def find_parent_folder_uid(name):
    f = find_parent_folder(name)
    if f:
        return f["uid"]

    raise RuntimeError("No UID found for path:" + name)

doc_folder_uid = find_parent_folder_uid("documentation")
gw_folder_uid  = find_parent_folder_uid("documentation/nexiles-gateway")
gws_folder_uid = find_parent_folder_uid("documentation/nexiles-gateway/gateway-services")

def create_doc(package_name, version, parent):
    icon_path = os.path.join(package_name, "icon.png")
    doc_url   = os.path.join(package_name, version, "index.html")
    zip_url   = os.path.join(package_name, "%s.zip" % version)
    create(parent, title=package_name, version=version, url=doc_url, zip=zip_url, icon=icon_path)

def create_or_update_content(parent, package):
    existing = find_docmeta(package["title"])

    operation = create
    uid = parent
    if existing:
        operation = update
        uid = existing["uid"]

    return operation(uid,
                     title=package["title"],
                     version=package["version"],
                     url=package["html_url"],
                     zip=package["zip_url"],
                     icon=package["icon_url"])


def publish_gws_docs():
    """
    docserver directory layout

    nexiles.gateway.services
        nexiles.gateway.fileservice
            v0.1
            v0.1.zip
        nexiles.gateway.query
            v0.1
            v0.1.zip

    dist layout

    /Users/seletz/Dropbox/dist/nexiles.gateway.services
    ├── attributeservice
    │   ├── nexiles.gateway.attributeservice-0.1
    │   ├── nexiles.gateway.attributeservice-0.1dev
    │   └── nexiles.gateway.attributeservice-0.2dev
    ├── collectorservice
    │   ├── nexiles.gateway.collectorservice-0.1
    │   └── nexiles.gateway.collectorservice-0.1dev
    ├── fileservice
    │   ├── nexiles.gateway.fileservice-0.1
    │   ├── nexiles.gateway.fileservice-0.1dev
    │   └── nexiles.gateway.fileservice-0.2dev
    ├── numberservice
    │   ├── nexiles.gateway.numberservice-0.1
    │   ├── nexiles.gateway.numberservice-0.1dev
    │   ├── nexiles.gateway.numberservice-0.2
    │   ├── nexiles.gateway.numberservice-0.2dev
    │   └── nexiles.gateway.numberservice-0.3dev
    ├── principalservice
    │   ├── nexiles.gateway.principalservice-0.1
    │   └── nexiles.gateway.principalservice-0.1dev
    ├── query
    │   ├── nexiles.gateway.query-0.1
    │   ├── nexiles.gateway.query-0.1dev
    │   ├── nexiles.gateway.query-0.2
    │   └── nexiles.gateway.query-0.2dev
    ├── reportservice
    │   ├── nexiles.gateway.reportservice-0.1
    │   ├── nexiles.gateway.reportservice-0.1dev
    │   └── nexiles.gateway.reportservice-0.2dev
    └── zipservice
        ├── nexiles.gateway.zipservice-0.1
        └── nexiles.gateway.zipservice-0.1dev
    """
    parent         = find_parent_folder_uid("documentation/nexiles-gateway/gateway-services")
    services       = "attributeservice collectorservice fileservice numberservice principalservice query reportservice zipservice".split()

    def find_doc_packages(services, dist_folder):
        packages = []

        def pkg_info(**kw):
            packages.append(kw)
            return kw

        for service in services:
            for d in glob.glob(os.path.join(dist_folder, "nexiles.gateway.services", service, "nexiles.gateway.%s*" % service)):
                bn = os.path.basename(d)
                basename, version = bn.split("-", 1)
                sd = os.path.join(d, "{0}-doc-{1}.tgz".format(basename, version))
                # print "       searching for: {0}".format(sd)
                for package in glob.glob(sd):
                    package_folder = os.path.dirname(package)
                    package_name = os.path.basename(package)

                    pkg = pkg_info(service=service, name=package_name, source=package_folder, path=package, version=version)

                    if "service" in service:
                        pkg["title"] = "nexiles|gateway {0} ({1})".format(service, version)
                    else:
                        pkg["title"] = "nexiles|gateway {0} ({1}) service".format(service, version)
                    pkg["html_url"] = ""
                    pkg["icon_url"] = ""
                    pkg["zip_url"] = ""

        return packages

    def publish_docserver(docserver_base, packages):
        for package in packages:
            print "Processing doc package {service}, version {version}.".format(**package)

            # nexiles.gateway.services/nexiles.gateway.fileservice
            docserver_package_base = os.path.join(docserver_base, "nexiles.gateway." + package["service"])

            # nexiles.gateway.services/nexiles.gateway.fileservice/0.1dev/index.html
            package["html_url"]    = os.path.join(docserver_package_base, package["version"], "index.html")

            # nexiles.gateway.services/nexiles.gateway.fileservice/0.1dev.zip
            package["zip_url"]     = os.path.join(docserver_package_base, "{0}.zip".format(package["version"]))

            # nexiles.gateway.services/icon.png
            package["icon_url"]    = os.path.join(docserver_base, "icon.png")

            # ~/Dropbox/docserver/docs/nexiles.gateway.services/nexiles.gateway.fileservice
            docserver_package_dir  = os.path.join(docserver_dist, docserver_package_base)

            with settings(hide("stdout", "running")):
                # extract HTML
                with lcd(package["source"]):
                    # local("ls -la {0}".format(package["name"]))
                    local("mkdir -p {0}/{1}".format(docserver_package_dir, package["version"]))
                    local("tar xzf {0} -C {1}/{2}".format(package["name"], docserver_package_dir, package["version"]))

                # repackage as zip
                with lcd(os.path.join(docserver_package_dir, package["version"])):
                    local("zip -r ../{0} .".format(os.path.basename(package["zip_url"])))

            # create plone content
            item = create_or_update_content(gws_folder_uid, package)
            print "    item url: {url}".format(**item["items"][0])

            package["item"] = item["items"][0]

    packages = find_doc_packages(services, dist_folder)
    print "Found %d packages." % len(packages)

    publish_docserver("nexiles.gateway.services", packages)

# vim: set ft=python ts=4 sw=4 expandtab :

