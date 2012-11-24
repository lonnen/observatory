import json

from flask import Blueprint, abort, jsonify
import requests

releases = Blueprint('releases', __name__, template_folder="templates")

@releases.route('/<name>')
def release(name):  
    ref = "refs/tags/v%s" % name
    tags = fetch_all_releases()
    for tag in tags:
        if tag['ref'] == ref:
            return jsonify({'version': fetch_tag(tag['object']['sha'])})
    return abort(404) # release name not found


@releases.route('/')
def released():
    return jsonify({'releases': fetch_all_releases()})


def _fetch(endpoint):
    """fetch the api endpoint and return the payload parsed into python objects

    endpoint - a url fragment to fetch
               ex: "/repose/mozilla/socorro/git/refs/tags"
    """
    url = 'https://api.github.com/repos/mozilla/socorro%s' % endpoint
    response = requests.get(url)
    if response.status_code is not 200:
        abort(424)
    return json.loads(response.text)

def fetch_tags():
    """fetch information about socorro tags from github"""
    return sorted(_fetch('/git/refs/tags'), version_comparator)

def fetch_all_releases():
    """fetch all tags from github and fake two upcoming release tags"""
    tags = fetch_tags()
    max_tag = get_version_tuple(tags[0])
    for _ in range(2):
        max_tag = [int(max_tag[0]) + 1,] + max_tag[1:]
        _next = '.'.join(map(str, max_tag))
        tags.insert(0, {
            'tag': 'v'+_next,
            'message': 'unreleased',
            'ref': "refs/tags/v%s" % _next 
        })
    return tags

def fetch_tag(sha):
    """fetch information about an individual tag from github"""
    return _fetch('/git/tags/%s' % sha)

def get_version_tuple(tag):
    """Parses a tag information into a version tuple
    
    tag - github api v3 tag object
            
    returns a tuple (major, [optional: minor], [optional: patch])
    """

    return tag['ref'].split('v')[-1].split('.')

def version_comparator(tagX, tagY):
    """Socorro version comparator suitable for passting to `sorted()`
    
    tagX - github api v3 tag object
    tagY - github api v3 tag object

    returns -1 or 0 or 1
    """
    get_version_tuple = lambda x: x['url'].split('v')[-1].split('.')
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
