"""
Django settings for erna project in DEV.
"""
import os
from pathlib import Path
from celery.schedules import crontab


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_DIR = os.path.dirname(BASE_DIR)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Django settings for projects

ALLOWED_HOSTS = ['*']

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = (
    'http://localhost:8080',
    'http://127.0.0.1:8080',
)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]



# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]



# other related path
PIPELINES_DIR = os.path.join(PROJECT_DIR, 'pipelines')

# third-party bioinformatics tools
EXTERNALS_DIR = os.path.join(PROJECT_DIR, 'externals')

# third-party bioinformatics tools
LOGS_DIR = os.path.join(PROJECT_DIR, 'logs')

# raw data namely fastq
RAW_DATA_DIRS = [os.path.join(PROJECT_DIR, 'raw_data'),]

# analytic results
RESULTS_DIR = os.path.join(PROJECT_DIR, 'results')

# reference namely genome DNA in fa format
REFERENCES_DIR = os.path.join(PROJECT_DIR, 'references')
INDEX_DIR = os.path.join(REFERENCES_DIR, 'index')
if not os.path.isdir(INDEX_DIR):
    os.mkdir(INDEX_DIR)


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
CELERYD_HIJACK_ROOT_LOGGER=True
