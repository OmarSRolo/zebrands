from decouple import config

celery_broker_url: str = config('BROKER_URL', default='redis://@127.0.0.1:6379')
celery_result_backend: str = 'django-db'
celery_accept_content: list[str] = ['json']
celery_task_serializer: str = 'json'
celery_result_serializer: str = 'json'
celery_timezone: str = 'America/Havana'
celery_task_track_started: bool = True
celery_result_extended: bool = True
# celery_beat_scheduler: str = 'django_celery_beat.schedulers:DatabaseScheduler'
broker_connection_retry_on_startup = True

# celery_beat_schedule: dict[str, Any] = {
#     'upload-logs-s3-task': {
#         'task': '',
#         'schedule': crontab(hour='5', minute='0'),  # ejecuta todos los dias a las 5 am
#     }
# }
