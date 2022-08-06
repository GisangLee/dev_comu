#!/usr/bin/env python
import os, dotenv
from config.settings.common import PROJ_DIR
import sys

ENV_DIR = os.path.join(PROJ_DIR, '.env')
print(f"ENV DIR: {ENV_DIR}")
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    dotenv.read_dotenv(ENV_DIR)
    main()
