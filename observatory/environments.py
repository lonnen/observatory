import json

import requests
import settings


def fetch_environments():
    """enumerates known environments"""
    return settings.ENVIRONMENTS

def fetch_environment(environment):
    """fetch and environment's status"""
    url = settings.ENVIRONMENTS.get(environment, None)
    if not url:
        print "No environment `%s` in settings" % environment
        return ""
    response = requests.get(url)
    if response.status_code is not 200:
        print "%s - %s" % (respose.status_code, url)
        return ""
    return json.loads(response.text)
