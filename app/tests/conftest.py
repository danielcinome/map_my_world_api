
from app.main import app
from fastapi.testclient import TestClient
import pytest
import os
from app.db.testing.engine import TestingManager
from app.db.postgres.engine import PostgresqlManager
from app.api.core.env_manager import EnvManager



app.dependency_overrides[PostgresqlManager.get_db] = TestingManager.get_db

@pytest.fixture
def client():
    yield TestClient(app)

@pytest.fixture
def auth_token(client):
    response = client.post('/login/access-token', data={
        'username': 'test_user',
        'password': 'test_password'
    })
    assert response.status_code == 200
    return response.json().get('access_token')

@pytest.fixture
def client_with_auth(auth_token):
    client = TestClient(app)
    client.headers.update({'Authorization': f'Bearer {auth_token}'})
    return client


def pytest_configure(config):
    TestingManager.create_db()

def pytest_sessionfinish(session, exitstatus):
    try:
        os.remove(EnvManager.TESTING_DB_URL.replace('sqlite:///', '').replace('?check_same_thread=False', ''))

    except OSError:
        pass