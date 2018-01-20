"""
Django settings for RRHH project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4b4s1+ikt+w7+(2(husp9vr@j0%&bt%j=gq69w460v@rp5nea&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ["*"]

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Application definition


SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'apps.helpers',
    'apps.configuraciones',
    'apps.vacaciones',
    'apps.biometrico',
    'apps.licencias',
    'apps.justificaciones',
    'django_sortable',
    'django_filters',
    'bootstrap3_datetime'
    #'easy_pdf',
    # Uncomment the next line to enable the admin:
    #'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    #'django.contrib.admindocs',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rrhh.middleware.AutoLogout',
)


AUTO_LOGOUT_DELAY = 15

ROOT_URLCONF = 'rrhh.urls'

WSGI_APPLICATION = 'rrhh.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'control_rrhh',
        'USER': 'rrhh',
        'PASSWORD': 'pass_rrhh',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Asuncion'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/



from unipath import Path
RUTA_PROYECTO = Path(__file__).ancestor(2)


STATIC_URL = '/static/'
STATIC_ROOT = RUTA_PROYECTO.child('static')

TEMPLATE_DIRS = (
    RUTA_PROYECTO.child('templates')
)

# *******************************

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))

TEMPLATE_DIRS = (os.path.join(PROJECT_PATH, '../templates'),)

# *******************************

STATICFILES_DIRS = (
    RUTA_PROYECTO.child('static'),
)

MEDIA_ROOT = RUTA_PROYECTO.child('media')
MEDIA_URL = 'http://192.168.100.103:80/media/'



TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

LOGIN_REDIRECT_URL = '/'