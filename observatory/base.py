import logging

from flask import Blueprint, current_app, json, request, Response, abort
from werkzeug.exceptions import NotFound

base = Blueprint("base", __name__)

@base.route("/ping")
def ping():
    return "pong"
