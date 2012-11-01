import logging
import logging.config
import os

from flask import (abort, current_app, Flask, jsonify, render_template,
                    request, Response)

from github import fetch_tags, fetch_tag
from socorro import (fetch_environment, fetch_environments,
                        fetch_most_recent_tag, get_version_tuple)


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
    #return jsonify(fetch_tags())
    return jsonify(fetch_environments())
    #return jsonify(fetch_environment('prod'))
    #return render_template('index.html')

@app.route("/versions/next")
def next_version():
    """answers what upcoming version will be the next release

    this should be the release candidate on the stage branch
    guessed with a simple heuristic of n+1 where n is our latest release
    """
    n = list(get_version_tuple(fetch_most_recent_tag()))
    n[0] = str(int(n[0]) + 1)
    return jsonify({'version': "".join(n)})

@app.route("/versions/dev")
def dev_version():
    """answers what version number is assigned to the current developer version

    this should be the version on the dev branch
    guessed with a simple heuristic of n+2 where n is our latest release
    """
    n = list(get_version_tuple(fetch_most_recent_tag()))
    n[0] = str(int(n[0]) + 2)
    return jsonify({'version': "".join(n)})
