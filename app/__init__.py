import os
import redis
from celery import Celery

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/1')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/1')
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')


def make_celery(app_name=__name__):
    return Celery('app', backend=CELERY_BROKER_URL, broker=CELERY_RESULT_BACKEND)


celery = make_celery()
db = redis.StrictRedis.from_url(REDIS_URL, decode_responses=True)
