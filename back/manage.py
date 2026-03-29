#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv


def main():
    """Run administrative tasks."""
    load_dotenv(Path(__file__).resolve().parent / ".env")
    settings_module = os.getenv("DJANGO_SETTINGS_MODULE")
    if not settings_module:
        mode = os.getenv("MODE", "DEV").upper()
        settings_module = "config.settings.prod" if mode == "PROD" else "config.settings.dev"
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        print("NOTE: Running format and lint checks before tests")
        project_dir = Path(__file__).resolve().parent
        for command in (
            ["black", str(project_dir)],
            ["isort", str(project_dir)],
            ["ruff", "check", str(project_dir)],
        ):
            result = subprocess.run(command, text=True, capture_output=True)
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
            if result.returncode != 0:
                sys.exit(result.returncode)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
