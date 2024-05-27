from .celery import app as celery_app

# загрузка при запуске Django
__all__ = ['celery_app']
