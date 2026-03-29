"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from pathlib import Path

from config.settings_selector import resolve_settings_module
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parent.parent / ".env")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", resolve_settings_module())

application = get_wsgi_application()
