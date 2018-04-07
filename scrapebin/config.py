import os
from configparser import ConfigParser

from scrapebin.constants import CONFIG_FILE


def _get_config():
    with open(CONFIG_FILE) as cf:
        config_parser = ConfigParser()
        config_parser.readfp(cf)
        return config_parser

cfg = _get_config()
