import os, dotenv
from config.settings.common import PROJ_DIR
from django.core.wsgi import get_wsgi_application


ENV_DIR = os.path.join(PROJ_DIR, '.env')
print(f"ENV DIR: {ENV_DIR}")

dotenv.read_dotenv(ENV_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')

application = get_wsgi_application()
