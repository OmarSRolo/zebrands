import os
import sys
from datetime import timedelta
from typing import Any

from decouple import config
from unipath import Path

# BASE_DIR
BASE_DIR = Path(__file__).ancestor(3)

SECRET_KEY: str = config("SECRET_KEY")

THIRD_PARTY_APPS: list[str] = [
    'rest_framework',
    'corsheaders',
    'storages',
]

LOCAL_APPS: list[str] = [
    "apps.auth_system",
    "apps.products",
    "apps.users",
    "apps.categories",
]

DJANGO_APP: list[str] = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs'
]

INSTALLED_APPS: list[str] = DJANGO_APP + LOCAL_APPS + THIRD_PARTY_APPS

ROOT_URLCONF: str = 'project.urls.urls'

TEMPLATES: list[dict[str, Any]] = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION: str = 'project.wsgi.application'

AUTH_USER_MODEL: str = "auth_system.Users"

PASSWORD_HASHERS: list[str] = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
]

# Password validation

AUTH_PASSWORD_VALIDATORS: list[dict[str, Any]] = [
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

# MIDDLEWARE

MIDDLEWARE: list[str] = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Internationalization

USE_I18N: bool = True

LOCALE_PATHS: list[str] = [
    BASE_DIR + '/locales'
]

ALLOWED_HOSTS: list[str] = ['*']

USE_L10N: bool = True

USE_TZ: bool = True

LANGUAGE_CODE: str = 'es'
TIME_ZONE: str = 'America/Havana'

DEFAULT_AUTO_FIELD: str = 'django.db.models.AutoField'

# Third party

# REDIS
USE_REDIS: bool = config("USE_REDIS", default=False, cast=bool)

USE_S3: bool = config("USE_S3", default=False, cast=bool)
if USE_S3:
    AWS_S3_REGION_NAME: str = config("AWS_S3_REGION_NAME")
    AWS_S3_ENDPOINT_URL: str = config("AWS_S3_ENDPOINT_URL")
    AWS_ACCESS_KEY_ID: str = config("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = config("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME: str = config("AWS_STORAGE_BUCKET_NAME")
    AWS_DEFAULT_ACL: str = 'public-read'
    AWS_QUERYSTRING_AUTH: bool = False

    STATIC_LOCATION: str = 'static'
    STATICFILES_STORAGE: str = 'apps.auth_system.storages.storages.StaticStorage'
    STATIC_URL: str = 'https://%s/%s/' % (AWS_S3_ENDPOINT_URL, 'static')

    PUBLIC_MEDIA_LOCATION: str = 'media'
    MEDIA_URL: str = 'https://%s/%s/' % (AWS_S3_ENDPOINT_URL, 'media')
    DEFAULT_FILE_STORAGE: str = 'apps.auth_system.storages.storages.PublicMediaStorage'

# DJANGO_REST_FRAMEWORK
ERROR_ORIGINAL: bool = config('ERROR_ORIGINAL', cast=bool, default=False)

REST_FRAMEWORK: dict[str, Any] = {
    'COERCE_DECIMAL_TO_STRING': True,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning'
}

AUTH_METHOD: str = "token"

SIMPLE_JWT: dict[str, Any] = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=config("ACCESS_TOKEN_LIFETIME", cast=int)),
    'REFRESH_TOKEN_LIFETIME': timedelta(hours=config("REFRESH_TOKEN_LIFETIME", cast=int)),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_CLAIM': 'id',
    'AUTH_HEADER_TYPES': ('Bearer', 'Token',),
}

ASGI_APPLICATION: str = 'project.asgi.application'

# Detect if executed under test
TESTING: bool = any(test in sys.argv for test in
                    ('test', 'csslint', 'jenkins', 'jslint', 'jtest', 'lettuce', 'pep8', 'pyflakes', 'pylint',
                     'sloccount',))

# CORS_HEADERS
CORS_ORIGIN_ALLOW_ALL: bool = True
CORS_ALLOW_CREDENTIALS: bool = True
CORS_ALLOW_HEADERS: list[str] = ["Authorization", "Content-Type", "X-CSRFToken", ]

# Email
EMAIL_BACKEND: str = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST: str = ''
EMAIL_HOST_USER: str = ''
EMAIL_HOST_PASSWORD: str = config("EMAIL_PASSWORD")
EMAIL_PORT: int = 587
EMAIL_USE_TLS: bool = True
DEFAULT_FROM_EMAIL: str = 'chicomtz.sr@gmail.com'
SERVER_EMAIL: str = ''

ADMINS: list[tuple[str, str]] = [('Omar', 'chicomtz.sr@gmail.com'), ]

# Static
STATICFILES_DIRS: tuple[str] = (os.path.join(BASE_DIR, 'static/admin'),)
STATIC_ROOT: str = os.path.join(BASE_DIR, 'static')
STATIC_URL: str = '/static/'

# Media
MEDIA_ROOT: str = os.path.join(BASE_DIR, 'media')
MEDIA_URL: str = '/media/'

# Kb
MAX_IMAGE_SIZE: int = int(config("MAX_IMAGE_SIZE", 100))
