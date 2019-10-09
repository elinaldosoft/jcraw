celery:
	celery -A celery_worker.celery worker --loglevel=info
server:
	python run.py
test:
	py.test