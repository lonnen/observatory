import logging
import logging.config
import os

from flask import Flask, render_template

from environments.environments import environments
from releases.releases import releases

app = Flask(__name__)
app.config.from_object("observatory.settings")

for setting, value in app.config.iteritems():
    if setting in os.environ:
        app.config[setting] = os.environ.get(setting, value)

logging_conf = app.config.get("LOGGING_CONF")
if logging_conf and os.path.exists(logging_conf):
    logging.config.fileConfig(logging_conf)

logger_name = app.config.get("LOGGER_NAME")

app.register_blueprint(environments, url_prefix='/environments')

app.register_blueprint(releases, url_prefix='/releases')
