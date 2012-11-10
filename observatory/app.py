import logging
import logging.config
import os

from flask import abort, Flask, jsonify, render_template

from github import fetch_tags, fetch_tag
from socorro import fetch_most_recent_tag, get_version_tuple


app = Flask(__name__)

app.config.from_object("observatory.settings")

if "OBSERVATORY_CONFIG" in os.environ:
    app.config.from_envvar("OBSERVATORY_CONFIG")

logging_conf = app.config.get("LOGGING_CONF")
if logging_conf and os.path.exists(logging_conf):
    logging.config.fileConfig(logging_conf)

logger_name = app.config.get("LOGGER_NAME")
if logger_name:
    logging.root.name = logger_name


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/branches")
def branches():
    return jsonify({'branches': ['dev', 'stage']})

@app.route("/branches/stage")
def stage_version():
    """answers what upcoming version will be the next release

    this should be the release candidate on the stage branch
    guessed with a simple heuristic of n+1 where n is our latest release
    """
    n = list(get_version_tuple(fetch_most_recent_tag()))
    n[0] = str(int(n[0]) + 1)
    return jsonify({'version': "".join(n)})


@app.route("/branches/dev")
@app.route("/branches/master")
def dev_version():
    """answers what version number is assigned to the current developer version

    this should be the version on the dev branch
    guessed with a simple heuristic of n+2 where n is our latest release
    """
    n = list(get_version_tuple(fetch_most_recent_tag()))
    n[0] = str(int(n[0]) + 2)
    return jsonify({'version': "".join(n)})


@app.route("/versions")
def fetch_versions():
    """answers all currently released versions.

    this does NOT include upcoming versions on dev and stage
    """
    return jsonify({"versions": fetch_tags()})


@app.route("/versions/<version>")
def fetch_version(version):
    """answers details about a specific version"""
    ref = "refs/tags/v%s" % version
    for tag in fetch_tags():
        if tag['ref'] == ref:
            return jsonify({'version': fetch_tag(tag['object']['sha'])})
    return abort(404)
