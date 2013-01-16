import json
from urlparse import urlparse

from flask import Blueprint, abort, current_app, jsonify, request
from werkzeug.contrib.cache import RedisCache

from observatory.exceptions import FailedDependency

import requests


environments = Blueprint('environments', __name__, template_folder="templates")


@environments.before_request
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


@environments.after_request
def cache_response(response):
    config = current_app.config
    redis_url = urlparse(config.get('REDISTOGO_URL', 'redis://localhost'))
    cache = RedisCache(host=redis_url.hostname, port=redis_url.port,
                       password=redis_url.password,
                       default_timeout=config.get('CACHE_TIMEOUT', 300))
    if not request.values:
        cache.set(request.path, response)
    return response


@environments.route('/<environment>')
def environ(environment='dev'):
    try:
        return jsonify(fetch_environ(environment))
    except KeyError:
        abort(404)


@environments.route('/')
def environs():
    envs = {}
    for env in current_app.config['ENVIRONMENTS'].keys():
        try:
            envs.update(fetch_environ(env))
        except FailedDependency, fd:
            envs.update({env: fd.description})
    return jsonify(envs)


def fetch_environ(environment):
    """Fetches a single environment from a URL specified in the config

    environment - a shorthand name specified in the config. ex: prod, stage

    returns a json blob of information about the current status of the environment
    
    raises KeyError iff the environment is not in the configuration
    raises FailedDependency iff the environment returns a non-200 response
    """
    url = current_app.config['ENVIRONMENTS'][environment]
    response = requests.get(url)
    if response.status_code is not 200:
        raise FailedDependency("Github returned status code %s" % response.status_code)
    return {environment: json.loads(response.text)}
