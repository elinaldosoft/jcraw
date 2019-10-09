import json
import re
from flask import request, jsonify, make_response
from flask import current_app as app
from flask import abort
from flask_restplus import Namespace, Resource, fields
from app import tasks
from app import db
from app.util import status_process

REGEX_PROCESS = r'(\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})'

api = Namespace('proccesses', description='Process', validate=True)
process = api.model('Process', {'number': fields.String(pattern=REGEX_PROCESS, description='Número do Processo')})


@api.route('/<string:tribunal>')
class Processes(Resource):
    def add_in_queue(self, tribunal, number):
        task = tasks.get_process.delay(tribunal, number)
        return jsonify(
            {
                'status': 'in_queue',
                'message': "Dentro de alguns minutos seu processo estará disponível para acompanhamento",
                'task': task.id,
                'url': f"api/v1/proccesses/{number}",
            }
        )

    @api.doc(params={'tribunal': 'Sigla do tribunal ex. TJAL, TJMS'})
    @api.expect(process)
    def post(self, tribunal):
        if tribunal not in app.config['SPIDERS'].keys():
            return make_response(
                jsonify({"message": "Desculpa, mas não coletamos dados desse tribual ainda :(", "status": "fail"}), 404
            )
        number = request.get_json().get('number')
        if status_process(db, number) == 'not_expired':
            return jsonify({"message": "Aguarde 6 hours para tentar atualizar esse processo", "status": 'not_expired'})
        elif status_process(db, number) == 'running':
            return jsonify({"message": "Esse processo já está na fila de extracão", "status": "running"})
        return self.add_in_queue(tribunal, number)


@api.route('/<string:proccess>')
class ProcessesView(Resource):
    def get(self, proccess):
        if not re.match(REGEX_PROCESS, proccess):
            return make_response(
                jsonify(
                    {
                        'message': 'Formato inválido, use a seguinte forma 0710802-55.2018.8.02.0001 para realizar pesquisas',
                        'status': 'fail',
                    }
                ),
                400,
            )

        if not db.exists(proccess):
            return make_response(jsonify({'message': 'Esse processo ainda não existe em nossa base', 'status': 'fail'}), 400)

        status = db.hget(proccess, 'status')
        data = db.hget(proccess, 'data') or str({})
        return jsonify({'status': status, 'data': json.loads(data)})
