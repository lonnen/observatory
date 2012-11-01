import json

import requests

def fetch(endpoint):
    """fetch the api endpoint and return the payload parsed into python objects

    endpoint - a url fragment to fetch
               ex: "/repose/mozilla/socorro/git/refs/tags"
    """
    url = 'https://api.github.com/repos/mozilla/socorro%s' % endpoint
    response = requests.get(url)
    if response.status_code is not 200:
        print "%s - %s" % (response.status_code, url)
        return ""
    return json.loads(response.text)

def fetch_tags():
    """fetch information about tags from github"""
    return fetch('/git/refs/tags')

def fetch_tag(sha):
    """fetch information about an individual tag"""
    return fetch('/git/tags/%s' % sha)
