"""
Django settings for fynd project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Carica le variabili d'ambiente
ENV_FILE = BASE_DIR / "config" / ".env.local"
load_dotenv(ENV_FILE)

# Usa le variabili d'ambiente nel progetto
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
DEBUG = os.getenv("DEBUG") == "True"

# ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    # for django-allauth
    'dj_rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account', 
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.apple',
    'dj_rest_auth.registration',
    # custom user model
    'fynder.apps.FynderConfig',
    # base django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third-party apps
    'corsheaders',
    'rest_framework.authtoken',
    'rest_framework',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    # my apps
    'info.apps.InfoConfig',
    'trip.apps.TripConfig',

]

MIDDLEWARE = [
    # base django middleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # CORS middleware
    'corsheaders.middleware.CorsMiddleware',
    # Django Allauth middleware
    'allauth.account.middleware.AccountMiddleware',
]

# social auth
AUTHENTICATION_BACKENDS = [
    # django-allauth # Default authentication
    'allauth.account.auth_backends.AuthenticationBackend',  # Allauth backend
    # default
    'django.contrib.auth.backends.ModelBackend',
]

SITE_ID = 1  # Make sure this matches the ID in your Django admin Sites framework


GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', 'GOOGLE_CLIENT_SECRET')
APPLE_CLIENT_ID = os.getenv('APPLE_CLIENT_ID', 'YOUR_APPLE_CLIENT_ID')
APPLE_CLIENT_SECRET = os.getenv('APPLE_CLIENT_SECRET', 'YOUR_APPLE_CLIENT_SECRET')
APPLE_TEAM_ID = os.getenv('APPLE_TEAM_ID', 'APPLE_TEAM_ID')
APPLE_KEY_ID = os.getenv('APPLE_KEY_ID', 'APPLE_KEY_ID')
APPLE_PRIVATE_KEY = os.getenv('APPLE_PRIVATE_KEY', 'APPLE_PRIVATE_KEY').replace('\\n', '\n')


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': GOOGLE_CLIENT_ID,
            'secret': GOOGLE_CLIENT_SECRET,
        },
    },
    'apple': {
        'APP': {
            'client_id': APPLE_CLIENT_ID,
            'secret': APPLE_CLIENT_SECRET,
            'certificate_key': APPLE_PRIVATE_KEY,
            'team_id': APPLE_TEAM_ID,
            'key': APPLE_KEY_ID,
        }
    },
}


CSRF_COOKIE_SECURE = False
CSRF_USE_SESSIONS = False



ROOT_URLCONF = 'fynd.urls'

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

WSGI_APPLICATION = 'fynd.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DATABASE_NAME"),
        'USER': os.getenv("DATABASE_USER"),
        'PASSWORD': os.getenv("DATABASE_PASSWORD"),
        'HOST': os.getenv("DATABASE_HOST"),
        'PORT': os.getenv("DATABASE_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

# Custom user model
AUTH_USER_MODEL = 'fynder.Fynder'

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# django-rest-auth
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'COERCE_DECIMAL_TO_STRING': False,
}

JWT_AUTH_HTTPONLY = os.getenv('JWT_AUTH_HTTPONLY', default=False)

REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'my-app-auth',
    'JWT_AUTH_REFRESH_COOKIE': 'my-refresh-token',
    'JWT_AUTH_HTTPONLY': JWT_AUTH_HTTPONLY,
}

# todo: to change and ask frutto
APP_LOGIN_CALLBACK_URL = 'fynd://fynd.it/'

SPECTACULAR_SETTINGS = {
    'TITLE': 'Fynd API',
    'DESCRIPTION': 'Fynd..',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': True,
    "SWAGGER_UI_SETTINGS": {
        "persistAuthorization": True,
    },
}

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = os.getenv("EMAIL_PORT", default=465)
EMAIL_USER = os.getenv("EMAIL_USER", default="FYND APP")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_FROM_NAME = os.getenv("EMAIL_FROM_NAME", default="example@example.com")
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", default=False)
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", default=True)

# static
STATIC_URL = '/static/'

# Se hai file statici extra, assicurati che siano correttamente inclusi
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Aggiungi questa riga se hai una cartella statica personalizzata
]

# Impostazione di STATIC_ROOT per quando esegui collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Add these settings after STATIC_ROOT configuration

# Media files (User uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=90),
    'AUTH_HEADER_TYPES': ('Bearer',),
}


CORS_ALLOWED_ORIGINS = [
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5175",
    "http://127.0.0.1:5175",
    "http://0.0.0.0:5175",
    "http://0.0.0.0:5174",
]

CSRF_TRUSTED_ORIGINS = [
    'http://0.0.0.0:5174',
    'http://localhost:5174',  # Se usi localhost
    'http://localhost:8000',
]



# 
# VIATOR_API_URL_TEST=https://sandbox.viator.com/partner
# VIATOR_API_KEY_TEST=59ac00cb-0e8a-49aa-aba9-4ac560addf54
# VIATOR_API_URL_PROD=https://api.viator.com/partner
# VIATOR_API_KEY_PROD=dc90da85-ca03-45fe-b6a5-9469f86ec88b
# VIATOR API
VIATOR_API_URL_TEST = os.getenv("VIATOR_API_URL_TEST")
VIATOR_API_KEY_TEST = os.getenv("VIATOR_API_KEY_TEST")
VIATOR_API_URL_PROD = os.getenv("VIATOR_API_URL_PROD")
VIATOR_API_KEY_PROD = os.getenv("VIATOR_API_KEY_PROD")
VIATOR_API_URL = VIATOR_API_URL_TEST
VIATOR_API_KEY = VIATOR_API_KEY_TEST
