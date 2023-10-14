from .base import *
import dj_database_url

ALLOWED_HOSTS = ["nilexglobalsolar.com", "web-production-f9a3.up.railway.app"]

SECRET_KEY = 'django-insecure-4+_(3$tx@69!2wigy35y*+=+@98nod7f3ky!@p@dj%y5n1gulx'


CSRF_TRUSTED_ORIGINS = ['https://nilexglobalsolar.com', "https://web-production-f9a3.up.railway.app"]

DATABASE_URL = os.getenv("DATABASE_URL")

DATABASES = {
        "default": dj_database_url.config(default=DATABASE_URL, conn_max_age=1800),
    }