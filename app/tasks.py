import json
from datetime import datetime
from flask import current_app as app
from app import celery
from app import db


@celery.task()
def get_process(tribunal: str, number: str):
    try:
        db.hmset(number, {'created_at': datetime.utcnow().timestamp(), 'status': 'running'})
        rsp = app.config['SPIDERS'].get(tribunal).get_process(number)
        db.hmset(number, {'data': json.dumps(rsp), 'updated_at': datetime.utcnow().timestamp(), 'status': 'ok'})
    except Exception as e:
        db.hmset(number, {'updated_at': datetime.utcnow().timestamp(), 'status': 'fail'})
        raise e
