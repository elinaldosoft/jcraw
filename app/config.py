import os
from flask import Flask
from app.routes import blueprint
from app.spiders import tjal, tjms

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, instance_relative_config=True)

app.register_blueprint(blueprint)
app.debug = os.environ.get('DEBUG', True)

app.port = os.environ.get('PORT', 5000)
app.host = os.environ.get('HOST', '0.0.0.0')

AGENTS = os.path.join(BASE_DIR, 'app', 'agents.txt')

app.config["JSONIFY_MIMETYPE"] = "application/json; charset=utf-8"

app.config['SPIDERS'] = {'tjal': tjal.TjAl(), 'tjms': tjms.TjMs()}
app.config['celery'] = {
    'imports': ('app.tasks',),
    'task_serializer': 'json',
    'result_serializer': 'json',
    'accept_content': ['json'],
}


def create_app(app, config_extra={}):
    app.config.update(config_extra)
    return app
