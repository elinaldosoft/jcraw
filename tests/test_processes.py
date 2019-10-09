import time
from tests.conftest import api_version


def test_invalid_tribunal_input(client):
    response = client.post(f"{api_version}/proccesses/tjsp", json={'number': '0710802-55.2018.8.02.0001'})
    assert response.status_code == 404
    assert response.content_type == 'application/json; charset=utf-8'
    assert response.status == '404 NOT FOUND'
    assert response.json == {'message': 'Desculpa, mas não coletamos dados desse tribual ainda :(', 'status': 'fail'}


def test_invalid_proccesses_input(client):
    response = client.post(f"{api_version}/proccesses/tmjp", json={'number': 'xxx'})
    assert response.json == {
        'errors': {'number': "'xxx' does not match '(\\\\d{7}-\\\\d{2}\\\\.\\\\d{4}\\\\.\\\\d\\\\.\\\\d{2}\\\\.\\\\d{4})'"},
        'message': 'Input payload validation failed',
    }


def test_send_process_to_queue_tjal(client):
    response = client.post(f"{api_version}/proccesses/tjal", json={'number': '0710802-55.2018.8.02.0001'})
    data = response.get_json()
    assert data['status'] == 'in_queue'
    assert data['url'] == 'api/v1/proccesses/0710802-55.2018.8.02.0001'
    assert data['message'] == 'Dentro de alguns minutos seu processo estará disponível para acompanhamento'
    time.sleep(5)


def test_find_proccess_in_tjal(client):
    response = client.get(f"{api_version}/proccesses/0710802-55.2018.8.02.0001")
    data = response.get_json()['data']
    grau_1 = data[0]['1_grau']
    assert grau_1['processo'] == '0710802-55.2018.8.02.0001'
    assert grau_1['partes_do_processo'] == [
        {'advogados': ['Vinicius Faria de Cerqueira'], 'autor': 'José Carlos Cerqueira Souza Filho'},
        {
            'advogados': ['Marcus Vinicius Cavalcante Lins Filho', 'Thiago Maia Nobre Rocha', 'Orlando de Moura Cavalcante Neto'],
            'reu': 'Cony Engenharia Ltda.',
        },
    ]


def test_send_process_to_queue_tjms(client):
    response = client.post(f"{api_version}/proccesses/tjms", json={'number': '0821901-51.2018.8.12.0001'})
    data = response.get_json()
    assert data['status'] == 'in_queue'
    assert data['url'] == 'api/v1/proccesses/0821901-51.2018.8.12.0001'
    assert data['message'] == 'Dentro de alguns minutos seu processo estará disponível para acompanhamento'
    time.sleep(5)


def test_find_proccess_in_tjms(client):
    response = client.get(f"{api_version}/proccesses/0821901-51.2018.8.12.0001")
    data = response.get_json()['data']
    grau_1 = data[0]['1_grau']
    assert grau_1['processo'] == '0821901-51.2018.8.12.0001'
    assert grau_1['juiz'] == 'Zidiel Infantino Coutinho'


def test_find_proccess_in_tjms_grau_2(client):
    client.post(f"{api_version}/proccesses/tjms", json={'number': '1412535-05.2019.8.12.0000'})
    time.sleep(5)
    response = client.get(f"{api_version}/proccesses/1412535-05.2019.8.12.0000")
    data = response.get_json()['data']
    grau_2 = data[1]['2_grau']
    assert grau_2['classe'] == 'Habeas Corpus Criminal'
