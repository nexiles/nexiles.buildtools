import os
import re
import datetime
import fileinput

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

@task
def reload(path=None):
    """reload -- trigger a nexiles|gateway servlet reload."""
    if path is None:
        path = "version"

    host = local('grep "^java.rmi.server.hostname" $WT_HOME/codebase/wt.properties | cut -d = -f2', capture=True)
    if not host:
        host = local('grep "^wt.rmi.server.hostname" $WT_HOME/codebase/wt.properties | cut -d = -f2', capture=True)
        if not host:
            raise RuntimeError("Can't determine hostname.")

    user = os.environ.get("WTUSER", "orgadmin")
    pw   = os.environ.get("WTPASS", "orgadmin")
    cmd  = "curl -i --user {user}:{pw} -X GET -H 'nexiles-gateway-reload: true' http://{host}/Windchill/servlet/nexiles/tools/{path}".format(user=user, pw=pw, host=host, path=path)
    print red("RELOADING: " + path)
    local(cmd)

