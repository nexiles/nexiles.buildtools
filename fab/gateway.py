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
def reload():
    """reload -- trigger a nexiles|gateway servlet reload."""
    host = local('grep "^java.rmi.server.hostname" $WT_HOME/codebase/wt.properties | cut -d = -f2', capture=True)
    user = os.environ.get("WTUSER", "orgadmin")
    pw   = os.environ.get("WTPASS", "orgadmin")
    cmd  = "curl -i --user {user}:{pw} -X GET -H 'nexiles-gateway-reload: true' http://{host}/Windchill/servlet/nexiles/tools/version".format(user=user, pw=pw, host=host)
    local(cmd)

