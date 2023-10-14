from .base import *


SECRET_KEY = 'django-insecure-4+_(3$tx@69!2wigy35y*+=+@98nod7f3ky!@p@dj%y5n1gulx'

ALLOWED_HOSTS = ['localhost']


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
