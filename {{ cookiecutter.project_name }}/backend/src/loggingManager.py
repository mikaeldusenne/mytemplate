import logging
from logging.config import dictConfig
import requests
from os import environ
# import json

from backend.src import helpers as h


debug = h.get_env_debug()


dictConfig({
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "format": f"[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        },
        "access": {
            "format": "%(message)s",
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "mail": {
            "class": "backend.MailLogger.AWSSESHandler",
            "formatter": "default",
            "level": "ERROR",
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            # "filename": "/var/log/gunicorn.error.log",
            "filename": "./logs/flask.error.log",
            "maxBytes": 100000,
            "backupCount": 10,
            "delay": "True",
        },
        "events_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": "./logs/events.log",
            "maxBytes": 100000,
            "backupCount": 1000,
            "delay": "True",
        },
        "access_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "access",
            "filename": "./logs/flask.access.log",
            "maxBytes": 100000,
            "backupCount": 10,
            "delay": "True",
        }
    },
    "loggers": {
        "gunicorn.error": {
            "handlers": ["console", "error_file", "mail"],
            "level": "INFO",
            "propagate": False,
        },
        "gunicorn.access": {
            "handlers": ["console", "access_file"],
            "level": "INFO",
            "propagate": False,
        },
        "events": {
            "handlers": ["events_file"],
            "propagate": False,
        },
        "errors": {
            "handlers": ["error_file", "mail"],
            "propagate": False,
        }
    },
    "root": {
        "level": "DEBUG" if debug else "INFO",
        "handlers": ["console"],
    }
})
