"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from pathlib import Path

from django.core.asgi import get_asgi_application
from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parent.parent / ".env")

settings_module = os.getenv("DJANGO_SETTINGS_MODULE")
if not settings_module:
	mode = os.getenv("MODE", "DEV").upper()
	settings_module = "config.settings.prod" if mode == "PROD" else "config.settings.dev"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

application = get_asgi_application()
