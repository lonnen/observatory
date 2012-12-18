import json
from urlparse import urlparse

from flask import Blueprint, abort, current_app, jsonify, request
from werkzeug.contrib.cache import RedisCache

import requests

releases = Blueprint('releases', __name__, template_folder="templates")


@releases.before_request
def return_cached():
    config = current_app.config
    redis_url = urlparse(config.get('REDISTOGO_URL', 'redis://localhost'))
    cache = RedisCache(host=redis_url.hostname, port=redis_url.port,
                       password=redis_url.password,
                       default_timeout=config.get('CACHE_TIMEOUT', 300))
    if not request.values:
        response = cache.get(request.path)
        if response:
            return response


@releases.after_request
def cache_response(response):
    config = current_app.config
    redis_url = urlparse(config.get('REDISTOGO_URL', 'redis://localhost'))
    cache = RedisCache(host=redis_url.hostname, port=redis_url.port,
                       password=redis_url.password,
                       default_timeout=config.get('CACHE_TIMEOUT', 300))
    if not request.values:
        cache.set(request.path, response)
    return response


@releases.route('/<name>')
def release(name):
    ref = "refs/tags/v%s" % name
    tags = fetch_all_releases()
    for tag in tags:
        if tag['ref'] == ref:
            try:
                return jsonify(fetch_tag(tag['object']['sha']))
            except KeyError:
                return jsonify(tag)
    return abort(404)  # release name not found


@releases.route('/')
def released():
    return jsonify({'releases': fetch_all_releases()})


def _fetch(endpoint):
    """fetch the api endpoint and return the payload parsed into python dicts

    endpoint - a url fragment to fetch
               ex: "/repose/mozilla/socorro/git/refs/tags"
    """
    url = 'https://api.github.com/repos/mozilla/socorro%s' % endpoint
    response = requests.get(url)
    if response.status_code is not 200:
        abort(424)
    return json.loads(response.text)


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
