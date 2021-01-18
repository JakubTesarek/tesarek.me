"""Main website endpoints."""

from aiohttp import web
from aiohttp_jinja2 import template

routes = web.RouteTableDef()


@routes.get('/', name='index')
@template('index.tpl.html')
async def index(request):
    """Display homepage."""
    db = request.app.db
    return {
        'articles': db.find_articles()
    }


@routes.get('/whoami', name='whoami')
@template('whoami.tpl.html')
async def whoami(request):
    """Display about me page."""
    pass


@routes.get(r'/articles/{stub:[-\w]+}', name='article')
@template('article.tpl.html')
async def article(request):
    """Display article."""
    db = request.app.db
    article = db.find_article(request.match_info['stub'])
    if not article:
        raise web.HTTPNotFound()

    return {
        'article': article
    }
