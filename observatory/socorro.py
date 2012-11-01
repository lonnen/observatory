import json

from github import fetch_tags

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

def fetch_most_recent_tag():
    """fetches the most recent tag for socorro"""
    get_version_tuple = lambda x: x['url'].split('v')[-1].split('.')
    def version_comparator(tagX, tagY):
        x, y = get_version_tuple(tagX), get_version_tuple(tagY)
        q = 0
        while q < len(x):
            if q == len(y):
                # x is 10.1, y is 10
                return -1
            x_q, y_q = float(x[q]), float(y[q])
            if x_q < y_q:
                return 1
            if x_q > y_q:
                return -1
            q += 1
        return 0
    return sorted(fetch_tags(), version_comparator)[0]

def get_version_tuple(tag):
    """returns the version tuple of a tag object"""
    return tag['url'].split('v')[-1].split('.')
