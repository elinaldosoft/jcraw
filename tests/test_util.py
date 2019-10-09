from app import util
from app import db


def test_get_item(client):
    assert util.get_item(1, ['Luke', 'Leia']) == 'Leia'
    assert util.get_item(2, ['Han', 'Vader']) == []


def test_split_process_number(client):
    assert util.split_process_number('0729987-16.2017.8.02.0001') == {
        'ordem': '0729987',
        'verificador': '16',
        'ano': '2017',
        'digito': '8',
        'tribunal': '02',
        'origem': '0001',
    }


def test_status_process(client):
    assert util.status_process(db, '0729987-16.2017.8.02.0001') == 'not_expired'


def test_agent_random(client):
    assert util.random_agent() in util.agents()
