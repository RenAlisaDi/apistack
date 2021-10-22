import os  # нужен для того чтобы брать конфигурацию с views
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stackoverflowapi.settings')

app = Celery('stackoverflowapi')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# redis это такая же база данных как postgres только она работает быстрее,
# потому что работает на нашей оперативной памяти, а postgres на жестком диске
