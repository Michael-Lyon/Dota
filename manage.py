import os
from pathlib import Path
import sys
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

DEBUG = False
load_dotenv(os.path.join(BASE_DIR, ".env"))

def main(environment):
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'myshop.settings.{environment}')

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
    print(os.getenv("DEBUG"))
    if str(os.getenv("DEBUG")) == "True":
        main(environment="local")
    else:
        main(environment="production")