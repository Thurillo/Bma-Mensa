#!/usr/bin/env python
"""
File: manage.py
Destinazione: Cartella Root del Progetto (Bma-Mensa/manage.py)
Questo è il file principale per eseguire comandi Django.
"""
import os
import sys


def main():
    """Run administrative tasks."""
    # Assicura che 'config.settings' sia il file di settings di default
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

