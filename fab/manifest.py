import uuid
import zipfile
import datetime
from hashlib import sha256

try:
    import json
except ImportError:
    import simplejson as json

from fabric.api import task
from fabric.api import local
from fabric.api import run
from fabric.api import cd
from fabric.api import lcd
from fabric.api import prefix
from fabric.api import put
from fabric.api import env
from fabric.api import prompt
from fabric.colors import green, yellow, red
from fabric.contrib.console import confirm

__all__ = ["manifest", "make_manifest_file", "generate_urn"]

from nxfab import eggs

@task
def generate_urn():
    """ generate a URN
    """
    return uuid.uuid4().urn

@task
def manifest():
    """print manifest file(s) for packages
    """
    for package, egg in eggs():
        print yellow("building manifest for %s" % package)
        mf = make_manifest_file(package, egg)
        print red("manifest: " + mf)

def generate_manifest(name, p, h=None):
    """generate_manifest(name, p, h) -> mapping

    Generates a mapping used as the manifest file.

    :param package:   a dotted package name, as in setup.py
    :param p:         the zip file with package content.
    :param h:         optional hash function to use.
    :returns:         the path to the created manifest file.
    """
    if h is None:
        h = sha256
    m = {}
    fh = m["files"] = {}
    order = []
    with zipfile.ZipFile(p) as zf:
        for fi in zf.filelist:
            order.append(fi.filename)

        hash_all = h()
        for fn in sorted(order):
            contents = zf.read(fn)
            hash_all.update(contents)
            fh[fn] = h(contents).hexdigest()


    m["name"] = name
    m["sum"] = hash_all.hexdigest()
    m["date"] = datetime.datetime.now().isoformat()
    return m

def make_manifest_file(package, egg):
    """make_manifest_file(package, egg) -> file path

    Generate a manifest file for the given package/egg combo.  The manifest
    file is created in the build dir using the package name as a basename.

    .. note:: The egg is expected to be in src/<<package>>/dist/<<egg>>

    :param package:   a dotted package name, as in setup.py
    :param egg:       the egg name -- including the version and platform tag.
    :returns:         the path to the created manifest file.
    """
    with lcd("src/"+ package):
        manifest = generate_manifest(package, "src/%s/dist/%s" % (package, egg))
        out = json.dumps(manifest, indent=4)

        mf_path = "%s/%s.json" % (env.build_dir, package.replace(".", "-"))
        with file(mf_path, "w") as mf:
            mf.write(out)

        return mf_path
