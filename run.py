# This file sets up and configures Django project for the
# PIT survey app and then runs the 'migrate' and 'runserver'
# manage.py commands.
import os
import django
from django.conf import settings
from django.core.management import call_command

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
settings.configure(
    BASE_DIR=BASE_DIR,
    DEBUG=True,
    DATABASES={
        "default": {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=(
        'survey',
        'django.contrib.auth',
        'django.contrib.admin',
        'django.contrib.contenttypes',
        'django.contrib.messages',
        'django.contrib.sessions',
        'django.contrib.staticfiles',
        'crispy_forms',
        'channels_redis',
        'django_plotly_dash.apps.DjangoPlotlyDashConfig',
    ),
    MIDDLEWARE=[
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates')]
            ,
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
    ],
    AUTH_PASSWORD_VALIDATORS=[
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
    ],
    ROOT_URLCONF='survey.urls',
    TIME_ZONE='UTC',
    USE_TZ=True,
    STATIC_URL='/static/',
    CRISPY_TEMPLATE_PACK='bootstrap4',
    X_FRAME_OPTIONS='SAMEORIGIN',
    CHANNEL_LAYERS={
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [('localhost', 6379),],
            }
        }
    },
    PLOTLY_COMPONENTS=[
        'dash_core_components',
        'dash_html_components',
        'dash_renderer',
        'dpd_components'
    ],
    LOGIN_REDIRECT_URL='/',
    LOGIN_URL='/login',
    EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend',
)
django.setup()

call_command('migrate')
call_command('runserver')
