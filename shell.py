# -*- coding: utf-8 -*-
import os
import json
import glob
import requests
import logging

from fabric.api import env, task, lcd, local, execute, settings, hide
from fabric.colors import green, yellow, red

import docserver

DOCSERVER_URL = "http://docs.nexiles.com"
username = "seletz"
password = "12345"

docserver_dist = os.path.expanduser("~/Dropbox/docserver/docs")
dist_folder    = os.path.expanduser("~/Dropbox/dist")

plone_api = docserver.API(DOCSERVER_URL, "plone", username, password)
docs_api  = docserver.API(DOCSERVER_URL, "docs", username, password)

docs_api.logger.setLevel(logging.DEBUG)

folders   = docserver.PloneFolders(plone_api)

projects  = docserver.Projects(docs_api)
projects.logger.setLevel(logging.DEBUG)

docmetas  = docserver.Docmetas(docs_api)
docmetas.logger.setLevel(logging.DEBUG)


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

    service_list = "attributeservice collectorservice fileservice numberservice principalservice query reportservice zipservice".split()

    def find_doc_packages(services, dist_folder):
        packages = []
        services = []

        def pkg_info(**kw):
            packages.append(kw)
            return kw

        def service_info(**kw):
            services.append(kw)
            return kw

        for service in service_list:
            print "service: ", service
            si = service_info(title="nexiles.gateway.%s" % service, github="https://github.com/nexiles/nexiles.gateway.%s" % service)

            for d in glob.glob(os.path.join(dist_folder, "nexiles.gateway.services", service, "nexiles.gateway.%s*" % service)):
                bn = os.path.basename(d)
                basename, version = bn.split("-", 1)
                sd = os.path.join(d, "{0}-doc-{1}.tgz".format(basename, version))
                print "       searching for: {0}".format(sd)
                for package in glob.glob(sd):
                    package_folder = os.path.dirname(package)
                    package_name = os.path.basename(package)

                    pkg = pkg_info(si=si, service=service, name=package_name, source=package_folder, path=package, version=version)

                    if "service" in service:
                        pkg["title"] = "nexiles|gateway {0} ({1})".format(service, version)
                    else:
                        pkg["title"] = "nexiles|gateway {0} ({1}) service".format(service, version)
                    pkg["html_url"] = ""
                    pkg["icon_url"] = ""
                    pkg["zip_url"] = ""

        return services, packages

    def publish_docserver(docserver_base, services, packages):
        gw_project = projects.find("id", "nexiles-gateway")
        assert gw_project

        for service in services:
            # create service projects
            existing = projects.find("title", service["title"])
            if existing:
                service["item"] = projects.update(existing["uid"], **service)
            else:
                service["item"] = projects.create(gw_project["uid"], **service)

        for package in packages:
            print "Processing doc package {service}, version {version}.".format(**package)
            service = package["si"]["item"]

            # nexiles.gateway.services/nexiles.gateway.fileservice
            docserver_package_base = os.path.join(docserver_base, "nexiles.gateway." + package["service"])

            # nexiles.gateway.services/nexiles.gateway.fileservice/0.1dev/index.html
            package["doc_url"]    = os.path.join(docserver_package_base, package["version"], "index.html")

            # nexiles.gateway.services/nexiles.gateway.fileservice/0.1dev.zip
            package["zip"]        = os.path.join(docserver_package_base, "{0}.zip".format(package["version"]))

            # nexiles.gateway.services/icon.png
            package["doc_icon"]   = os.path.join(docserver_base, "icon.png")

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
            existing = docmetas.find("title", package["title"])
            if existing:
                package["item"] = docmetas.update(existing["uid"], **package)
            else:
                package["item"] = docmetas.create(service["uid"], **package)
            print "    docmeta package: {doc_url}".format(**package["item"])

    services, packages = find_doc_packages(service_list, dist_folder)
    print "Found %d services." % len(services)
    print "Found %d packages." % len(packages)

    publish_docserver("nexiles.gateway.services", services, packages)

# vim: set ft=python ts=4 sw=4 expandtab :

