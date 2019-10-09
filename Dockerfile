FROM python:3

ENV CELERY_BROKER_URL redis://redis:6379/1
ENV CELERY_RESULT_BACKEND redis://redis:6379/1
ENV REDIS_URL redis://redis:6379/0

ENV HOST 0.0.0.0
ENV PORT 5000
ENV DEBUG true

RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN apt-get install -y python3-dev
RUN python -m pip install --upgrade pip

WORKDIR /usr/src/app
EXPOSE 5000

COPY . .
RUN python -m pip install -r requirements/prod.txt

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "wsgi:app"]