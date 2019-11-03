"""
Django settings for recommender_service project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import json
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from datetime import datetime

from celery.schedules import crontab
from django.utils.log import DEFAULT_LOGGING



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(BASE_DIR+"/conf/recommender.json") as json_data:
    JSON_SETTING=json.load(json_data)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')r9231!z_psg4b3npcgod^)0kctegape-bdo3+df6#q)z%#-x6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ["*"]

MEDIA_URL = '/media/'

FILE_DIR = JSON_SETTING.get('FILE_DIR') if JSON_SETTING.get('FILE_DIR') else os.path.dirname(os.path.dirname((BASE_DIR)))
MEDIA_ROOT = os.path.join(FILE_DIR, 'media')
# Application definition
SWAGGER_SETTINGS = JSON_SETTING.get('SWAGGER_SETTINGS')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'django_cron',
    'applications.recommendation',
    'applications.notification'
]

REST_FRAMEWORK ={
    'DEFAULT_PERMISSION_CLASSES':('rest_framework.permissions.AllowAny',),
    "DEFAULT_AUTHENTICATION_CLASSES":(
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication'
                                      ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_xml.parsers.XMLParser',
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
    ),

}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'recommender_service.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.media',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'recommender_service.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = JSON_SETTING['DATABASES']
SESSION_COOKIE_DOMAIN = ["*"]
# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
USE_TZ = True
# Celery settings
CELERY_BROKER_URL = JSON_SETTING["CELERY_BROKER_URL"]
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_BROKER_POOL_LIMIT = None
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_ENABLE_UTC = False
MM = JSON_SETTING['notification']['sheduled']['minute']
HH = JSON_SETTING['notification']['sheduled']['hour']
DOW = JSON_SETTING['notification']['sheduled']['day_of_week']
CELERY_BEAT_SCHEDULE = {
    "sheduled_notification":{
        'task':'applications.notification.tasks.sheduled_notification',
         'schedule': crontab(minute=MM, hour=HH,day_of_week=DOW),
        'kwargs':{'from_csv':True}
    }
}
# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#STATIC_ROOT = os.path.join(BASE_DIR, "static")
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]
STATIC_URL = '/static/'

DEFAULT_LOGGING['handlers']['console']['filters']=[]
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': ' v1.0.4 %(levelname)s %(asctime)s %(process)d %(thread)d %(name)s:%(lineno)s:%(funcName)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s  %(name)s:%(lineno)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
     },

    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            #'filters':['require_debug_false'],
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'prod_console':{
            'filters':['require_debug_false'],
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'recommender_service': {
            'handlers': ['console','prod_console'],
            'level': DEBUG,
            'propagate': False,

        },
    }
}

# Django Cron Settings
CRON_CLASSES = [
    "applications.notification.crons.PersonaNotificationCron",
]

# Notification Settings
NOTIFICATION = JSON_SETTING['notification']

