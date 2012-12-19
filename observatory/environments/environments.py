import json

from flask import Blueprint, abort, current_app, jsonify
import requests

environments = Blueprint('environments', __name__, template_folder="templates")


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
