import os, dotenv
from django.core.wsgi import get_wsgi_application


ENV_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
dotenv.read_dotenv(ENV_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')

application = get_wsgi_application()
