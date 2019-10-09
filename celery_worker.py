from app import celery
from app import config
from app.celery import init_celery

app = config.create_app(config.app)
init_celery(celery, app)
