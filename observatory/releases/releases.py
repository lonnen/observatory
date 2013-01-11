import json
from urlparse import urlparse

from flask import Blueprint, abort, current_app, jsonify, request
from werkzeug.exceptions import HTTPException

import redis
import requests

releases = Blueprint('releases', __name__, template_folder="templates")


class FailedDependency(HTTPException):
    code = 424
    description = ("The request failed due to failure of a previous request.")
    name = "Failed Dependency"
    def get_response(self, environment):
        resp = super(FailedDependency, self).get_response(environment)
        resp.status = "%s %s" % (self.code, self.name.upper())
        return resp


@releases.route('/<name>')
def release(name):
    """fetch a json object with information about release `name`

    name - a socorro version, with or without the leading v
    """
    name = name[1:] if name.startswith('v') else name
    ref = "refs/tags/v%s" % name
    tags = fetch_all_releases()
    for tag in tags:
        if tag['ref'] == ref:
            try:
                return jsonify(fetch_tag(tag['object']['sha']))
            except KeyError:
                return jsonify(tag)
    raise FailedDependency # release name not found


@releases.route('/')
def released():
    releases = []
    for r in fetch_all_releases():
        name = r['ref'].split('v')[1]
        releases.append(json.loads(release(name).response[0]))
    return jsonify({'releases': fetch_all_releases()})


def _fetch(endpoint):
    """fetch the api endpoint and return the payload parsed into python dicts

    endpoint - a url fragment to fetch
               ex: "/repos/mozilla/socorro/git/refs/tags"
    """
    redis_url = urlparse(current_app.config.get('REDISTOGO_URL'))
    r = redis.StrictRedis(host=redis_url.hostname, port=redis_url.port)
    url = 'https://api.github.com/repos/mozilla/socorro%s' % endpoint

    cached = json.loads(r.get(url)) if r.get(url) else {}

    headers = {}
    if 'Last-Modified' in cached:
        headers = {'If-Modified-Since': cached['Last-Modified']}
    response = requests.get(url, headers=headers)

    if response.status_code == 304:
        return cached['json']
    if response.status_code == 200:
        dump = json.dumps({'Last-Modified': response.headers['Last-Modified'],
                           'json': response.json})
        r.set(url, dump)
        return response.json
    #raise FailedDependency
    abort(424)


def fetch_tags():
    """Fetch information about socorro tags from Github

    return a sorted list of tag dicts
    """
    return sorted(_fetch('/git/refs/tags'), version_comparator)


def fetch_all_releases():
    """Fetch all tags from github and fake two upcoming release tags

    returns a list of tag dicts prepended with fake release tag-like dicts
    """
    tags = fetch_tags()
    max_tag = get_version_tuple(tags[0])
    for _ in range(2):
        max_tag = [int(max_tag[0]) + 1, ] + max_tag[1:]
        _next = '.'.join(map(str, max_tag))
        tags.insert(0, forge_tag(_next))
    return tags


def fetch_tag(sha):
    """Fetch information about an individual tag from Github

    sha - sha of the git tag

    return a dictionary with attributes of the tag object
    """
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


def forge_tag(version):
    """Create a fake tag. Useful for future versions.

    version - version number to fake

    returns dictionary structured like a fake tag
    """
    return {
        'tag': 'v%s' % version,
        'message': 'unreleased',
        'ref': "refs/tags/v%s" % version
    }
