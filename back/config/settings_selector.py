"""Helpers for selecting Django settings module by environment mode."""

import os


MODE_TO_SETTINGS = {
    "DEV": "config.settings.dev",
    "PROD": "config.settings.prod",
}


def resolve_settings_module() -> str:
    explicit_module = os.getenv("DJANGO_SETTINGS_MODULE")
    if explicit_module:
        return explicit_module

    mode = os.getenv("MODE", "DEV").upper()
    return MODE_TO_SETTINGS.get(mode, MODE_TO_SETTINGS["DEV"])

