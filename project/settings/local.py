from .base import *

INSTALLED_APPS += ['drf_yasg', ]

DEBUG = config('DEBUG', default=True, cast=bool)

SWAGGER_SETTINGS: dict[str, Any] = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}
