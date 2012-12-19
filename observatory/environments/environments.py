import json
from urlparse import urlparse

from flask import Blueprint, abort, current_app, jsonify, request
from werkzeug.contrib.cache import RedisCache

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
        url = current_app.config['ENVIRONMENTS'][environment]
        response = requests.get(url)
        if response.status_code is not 200:
            abort(424)
        return jsonify({environment: json.loads(response.text)})
    except KeyError:
        abort(404)


@environments.route('/')
def environs():
    envs = {}
    for env in current_app.config['ENVIRONMENTS'].keys():
        envs.update(json.loads(environ(env).response[0]))
    return jsonify(envs)
