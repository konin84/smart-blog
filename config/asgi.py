"""
ASGI config for the config project.
Only needed if you add async features later (e.g. websockets via Channels).
gunicorn + WSGI (wsgi.py) is sufficient for this project as-is.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_asgi_application()
