"""Configuration methods."""

import json


def read_conf(path):
    """Return json conf parsed to a dictionary."""
    with open(path) as json_file:
        data = json_file.read()
        return json.loads(data)
