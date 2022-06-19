import logging.config
import sys

config = {
    "version": 1,
    "formatters": {
        "message": {"format": "%(asctime)s - %(message)s"},
        "verbose": {
            "format": "%(asctime)s - %(name)s.%(lineno)s - %(levelname)s - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": logging.INFO,
            "formatter": "message",
            "stream": sys.stdout,
        },
    },
    "root": {"level": logging.DEBUG, "handlers": ["console"]},
}
logging.config.dictConfig(config)
