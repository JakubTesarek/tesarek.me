"""Entry point for web application."""

from web.app import WebApplication


app = WebApplication({
    'debug': True
})
