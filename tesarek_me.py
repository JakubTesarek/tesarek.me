"""Entry point for web application."""

from web.app import WebApplication
from web.conf import read_conf
import os


async def app():
    conf = read_conf(os.environ.get('TESAREK_ME_CONF_PATH', 'local.conf.json'))
    return WebApplication(conf)
