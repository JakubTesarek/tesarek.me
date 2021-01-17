"""Frontend web application."""

import asyncio
import logging
import traceback

import aiohttp_jinja2
import aiohttp_debugtoolbar
import aiohttp_session
import aiohttp_session_flash
from aiohttp import web
from aiohttp_session import SimpleCookieStorage
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from jinja2 import PackageLoader, select_autoescape

from web import endpoints

logger = logging.getLogger(__name__)



@web.middleware
async def error_handler(request, handler):
    """Translate endpoint exceptions to json error response for user."""
    try:
        return await handler(request)
    except web.HTTPNotFound:
        return aiohttp_jinja2.render_template(
            'errors/404.tpl.html', request, {}, status=404
        )
    except web.HTTPException as e:
        raise e
    except asyncio.CancelledError:  # pragma: no cover
        logger.info('Requst canceled by user.')
        return aiohttp_jinja2.render_template(
            'errors/400.tpl.html', request, {}, status=400
        )
    except Exception:  # pragma: no cover
        logger.error(traceback.format_exc())
        return aiohttp_jinja2.render_template(
            'errors/500.tpl.html', request, {}, status=500
        )


class WebApplication(web.Application):
    """Web Application."""

    def __init__(self, conf):
        super().__init__()
        self.conf = conf
        self.setup_sessions()  # must be first of setup methods
        self.setup_error_handlers()
        self.setup_template_environment()
        self.setup_debug_toolbar()  # must be last of setup methods
        self.add_routes()

    def setup_error_handlers(self):
        """Adds error handlers."""
        self.middlewares.append(error_handler)

    def setup_debug_toolbar(self):
        """Initializes debug toolbar if app runs in debug mode."""
        if self.conf.get('debug'):  # pragma: no cover
            # This must be called AFTER aiohttp_session middleware, it intercepts cookies
            aiohttp_debugtoolbar.setup(self, intercept_redirects=False)

    def setup_template_environment(self):
        """Prepares template environment."""
        self.templates = aiohttp_jinja2.setup(
            self,
            loader=PackageLoader(__package__, 'templates'),
            autoescape=select_autoescape(['html']),
            context_processors=[
                aiohttp_session_flash.context_processor
            ]
        )

    def setup_sessions(self):
        """Add handlers for handling sessions and flash messages."""
        if self.conf['debug']:
            cookie_storage = SimpleCookieStorage()
        else:  # pragma: no cover
            secret_key = base64.urlsafe_b64decode(
                self.conf['session_key'].encode('utf-8')
            )
            cookie_storage = EncryptedCookieStorage(secret_key)

        self.middlewares.append(
            aiohttp_session.session_middleware(cookie_storage)
        )
        self.middlewares.append(
            aiohttp_session_flash.middleware
        )

    def add_routes(self):
        """Register all endpoint routes."""
        self.router.add_routes(endpoints.routes)
        self.router.add_routes([web.static('/static', f'{__package__}/static')])