import json
import logging
import logging.config
import os

from flask import Flask, current_app, json, request, Response, abort, render_template

from github import fetch_tags, fetch_tag
from environments import fetch_environment, fetch_environments

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
    #return json.dumps(fetch_tags())
    return json.dumps(fetch_environments())
    #return json.dumps(fetch_environment('prod'))
    #return render_template('index.html')
