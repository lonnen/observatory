import logging
import logging.config
import os

from flask import abort, Flask, jsonify, render_template

from environments.environments import environments
from releases.releases import releases

app = Flask(__name__)
app.config.from_object("observatory.settings")
if "OBSERVATORY_CONFIG" in os.environ:
    app.config.from_envvar("OBSERVATORY_CONFIG")

logging_conf = app.config.get("LOGGING_CONF")
if logging_conf and os.path.exists(logging_conf):
    logging.config.fileConfig(logging_conf)

logger_name = app.config.get("LOGGER_NAME")

app.register_blueprint(environments, url_prefix='/api/environments')
app.register_blueprint(releases, url_prefix='/api/releases')

@app.route("/")
def index():
    return render_template('index.html')
