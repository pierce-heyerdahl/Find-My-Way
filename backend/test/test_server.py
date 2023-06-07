from backend.server import app
from backend.models import *
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client
    
def test_main(client):
    response = client.get('/')
    assert response.status_code == 200

def test_admin_login(client):
    response = client.get('/adminLogin')
    assert response.status_code == 200