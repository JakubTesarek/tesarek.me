"""Main website endpoints."""

from aiohttp import web
from aiohttp_jinja2 import template

routes = web.RouteTableDef()

@routes.get('/', name='index')
@template('index.tpl.html')
async def index(request):
    """Display homepage."""
    pass
