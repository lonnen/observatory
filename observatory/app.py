import logging
import logging.config
import os

from flask import Flask


app = Flask("observatory")

app.config.from_object("observatory.settings")

if "OBSERVATORY_CONFIG" in os.environ:
    app.config.from_envvar("OBSERVATORY_CONFIG")

logging_conf = app.config.get("LOGGING_CONF")
if logging_conf and os.path.exists(logging_conf):
    logging.config.fileConfig(logging_conf)

logger_name = app.config.get("LOGGER_NAME")
if logger_name:
    logging.root.name = logger_name

app.register_blueprint(base)
