from redis import Connection
from datetime import datetime, timedelta
import functools
import re
import random
from app import config

STATUS = {1: 'ok', 2: 'running', 3: 'fail', 4: 'not_expired'}


def status_process(db: Connection, number: str) -> bool:
    if db.exists(number):
        data = db.hmget(number, 'status', 'updated_at')
        if data[0] == STATUS.get(1) and (datetime.fromtimestamp(float(data[1])) + timedelta(hours=6)) > datetime.utcnow():
            return STATUS.get(4)
        elif data[0] == STATUS.get(2):
            return STATUS.get(2)


def split_process_number(number: str) -> dict:
    process_number = re.search(
        r"(?P<ordem>\d{7})-(?P<verificador>\d{2})\.(?P<ano>\d{4})\.(?P<digito>\d)\.(?P<tribunal>\d{2})\.(?P<origem>\d{4})", number
    )
    return {
        'ordem': process_number.group('ordem'),
        'verificador': process_number.group('verificador'),
        'ano': process_number.group('ano'),
        'digito': process_number.group('digito'),
        'tribunal': process_number.group('tribunal'),
        'origem': process_number.group('origem'),
    }


def get_item(pos: int, itens: list) -> list:
    try:
        return itens[pos]
    except IndexError:
        return []


@functools.lru_cache(maxsize=128)
def agents():
    return open(config.AGENTS, 'r').read().splitlines()


def random_agent():
    return random.choice(agents())
