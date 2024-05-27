import os

from celery import Celery

# для встроенной в Celery программы командной строки celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')
app = Celery('myshop')
# настройки будут задаваться в файле settings.py c префексом CELERY_
# пример: CELERY_BROKER_URL = ...
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()  # Автоматическое обнаружение асинхронных задач в INSTALLED_APPS (tasks.py)
