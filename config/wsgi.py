"""
WSGI config for the config project.
Used by gunicorn / any traditional WSGI server in production.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()
