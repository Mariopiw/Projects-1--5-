from celery import Celery

from app.config import settings

celery_app = Celery("ops", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    beat_schedule={
        "escalate-open-exceptions-every-minute": {
            "task": "app.tasks.jobs.escalate_open_exceptions",
            "schedule": 60.0,
        }
    },
)
