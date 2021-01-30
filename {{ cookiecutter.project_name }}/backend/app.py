from flask import Flask, render_template, jsonify, redirect, flash, request, url_for, Response, Blueprint
import flask
import logging
import json
import numpy as np
import pandas as pd
import traceback
from pprint import pprint
from os import environ
import os

from backend.src.pytypes import *
import backend.src.helpers as h
import backend.src.db as db


def logging_setup(path):
    loggingdest = os.path.join(path, "flask.log")
    print("setting logging to {}".format(loggingdest))

    logFormatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    # format='%(asctime)s\t%(name)s\t%(funcName)s\t%(levelname)s\t%(message)s'
    rootLogger = logging.getLogger('{{cookiecutter.project_name}}')
    rootLogger.setLevel(logging.DEBUG if os.environ.get(
        "PROD", False) else logging.WARNING)

    fileHandler = logging.FileHandler(loggingdest)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)


logging_setup(".")


flsk = Blueprint(
    'bprnt', __name__,
    static_folder='./backend/static',
)

@flsk.route("/status", methods=["GET"])
def health_check():
    logging.debug("debug log")
    logging.info("info log")
    logging.warning("warning log")
    logging.error("error log")
    # logging.exception("exception log")
    return make_response("OK", 200)


@flsk.route('/', defaults={'path': ''})
@flsk.route('/<path:path>')
def index(path):
    return render_template('index.html')


app = Flask(__name__, static_url_path="/{{cookiecutter.root_url}}/static")
app.register_blueprint(flsk, url_prefix="{{cookiecutter.root_url}}")


db.connect()
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(host="0.0.0.0", debug=True)
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(logging.DEBUG)
    logging = app.logger
