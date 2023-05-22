"""Logging module for the project."""


import logging


logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s | %(levelname)s | %(message)s",
                    datefmt='%Y-%m-%d %H:%M:%S')

log = logging.getLogger(__name__)
