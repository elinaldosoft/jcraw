import pytest
from datetime import datetime
from app import config
from app import db
from app.routes import API_VERSION

api_version = f"/api/{API_VERSION}"

db.delete('0710802-55.2018.8.02.0001', '1412535-05.2019.8.12.0000', '0821901-51.2018.8.12.0001')
db.hmset('0729987-16.2017.8.02.0001', {'updated_at': datetime.utcnow().timestamp(), 'status': 'ok'})


@pytest.fixture
def app(request):
    app = config.create_app(config.app, {"TESTING": True})
    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()
