"""
Django settings for erna project in DEV.
"""
import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv('.env.dev'))
from celery.schedules import crontab
import json

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG')

# Access hosts
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1', 
    # host name defined in nginx conf
    'app',
    'vue_nginx',
]

# cross origin
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    'http://localhost:8080',
    'http://127.0.0.1:8080',
    # 'http://app',
]
CORS_ALLOW_CREDENTIALS = True

# csrf token
# CSRF_TRUSTED_ORIGINS = [
#     'http://localhost:8080',
#     'http://127.0.0.1:8080',
# ]
# allow CSRF cookie by HTTP
CSRF_COOKIE_SECURE = False

# session secure
SESSION_COOKIE_SECURE = False


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_dev.sqlite3',
    }
}


# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')



#celery settings
CELERY_BROKER_URL="redis://127.0.0.1:6379"
CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_EXTENDED = True
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = "America/New_York"
CELERY_ALWAYS_EAGER = True
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_BEAT_SCHEDULE = {
    "schedule_task": {
        "task": "celery_tasks.tasks.schedule_task",
        "schedule": crontab(minute="*/1"),
    },
}
