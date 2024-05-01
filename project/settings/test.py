from .base import *

DEBUG = config('DEBUG', default=False, cast=bool)

DATABASES: dict[str, Any] = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'zebrands.sqlite3',
    },
}
# FIXTURE
FIXTURE_DIRS: list[str] = [
    os.path.join(BASE_DIR, 'fixtures/'),
    os.path.join(BASE_DIR, 'apps/products/tests/fixtures/'),
    os.path.join(BASE_DIR, 'apps/auth_system/tests/fixtures/'),
    os.path.join(BASE_DIR, 'apps/users/tests/fixtures/'),
    os.path.join(BASE_DIR, 'apps/categories/tests/fixtures/'),
]

# CELERY
celery_broker_url: str = 'memory://'
celery_accept_content: list[str] = ['json']
celery_task_serializer: str = 'json'
celery_result_serializer: str = 'json'
celery_timezone: str = 'America/Havana'
celery_task_track_started: bool = True
celery_result_extended: bool = True
broker_connection_retry_on_startup = True
