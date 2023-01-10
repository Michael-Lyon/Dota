"""
Django settings for myshop project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path
import cloudinary
# import cloudinary.uploader
# import cloudinary.api
import environ

import django_heroku
from braintree import Configuration, Environment
from django.utils.translation import gettext_lazy as _

from python_paystack.paystack_config import PaystackConfig

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4+_(3$tx@69!2wigy35y*+=+@98nod7f3ky!@p@dj%y5n1gulx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'moma-dota.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',
    'cart',
    'orders',
    'payment',
    'coupons',
    'python_paystack',
    "django_makemessages_xgettext",
    'widget_tweaks',
    'cloudinary',
    'cloudinary_storage',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR/"templates", ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'cart.context_processors.cart',
                'shop.views.categories',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', _('English')),
    ('es', _('Spanish')),
)

LOCALE_PATHS = [

    (BASE_DIR / 'locale'),
]


TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
django_heroku.settings(locals())

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_PORT = 25
# EMAIL_HOST = 'smtp.freesmtpservers.com'
CART_SESSION_ID = 'cart'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.elasticemail.com'
EMAIL_HOST_PASSWORD = 'D4A140F2C3F11D6DE37E638412497D92EB52'
EMAIL_PORT = 2525
EMAIL_HOST_USER = 'mickiasomg@gmail.com'
EMAIL_USE_TLS = True

# PAYMENT SETTINGS
BRAINTREE_MERCHANT_ID = env("BRAINTREE_MERCHANT_ID")
BRAINTREE_PUBLIC_KEY = env("BRAINTREE_PUBLIC_KEY")
BRAINTREE_PRIVATE_KEY = env("BRAINTREE_PRIVATE_KEY")

Configuration.configure(
    Environment.Sandbox,
    BRAINTREE_MERCHANT_ID,
    BRAINTREE_PUBLIC_KEY,
    BRAINTREE_PRIVATE_KEY
)

#REDIS
REDIS_HOST = env("REDIS_HOST")
REDIS_PORT = env("REDIS_PORT")
REDIS_PASSWORD = env("REDIS_PASSWORD")
REDIS_DB = env("REDIS_DB")
# REDIS_DB = 1
 

PaystackConfig.SECRET_KEY = env("PAYSTACK_SECRET")
PaystackConfig.PUBLIC_KEY = env("PAYSTACK_PUBLIC")


cloudinary.config(
    cloud_name="dzy2mpv8w",
    api_key="896867796834272",
    api_secret="1OUOyOgQSrNta8J9In3Go8BkgN0",
    api_proxy="http://proxy.server:3128"
)


CLOUDINARY_URL="cloudinary://896867796834272:1OUOyOgQSrNta8J9In3Go8BkgN0@dzy2mpv8w"

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': "dzy2mpv8w",
    'API_KEY':  "896867796834272",
    'API_SECRET':  "1OUOyOgQSrNta8J9In3Go8BkgN0",
    'API_PROXY': "http://proxy.server:3128"
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
