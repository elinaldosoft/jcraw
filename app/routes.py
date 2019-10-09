from flask import Blueprint
from flask_restplus import Api
from app.controllers.processes import api as process_api

API_VERSION = 'v1'

blueprint = Blueprint('api', __name__, url_prefix=f"/api/{API_VERSION}")
api = Api(blueprint, doc='/docs')
api.add_namespace(process_api)
