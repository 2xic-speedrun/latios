import pytest
from .Service import app as real_app
import tempfile
import urllib.parse

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture()
def app():
    file = tempfile.NamedTemporaryFile()
    real_app.config.update({
        "TESTING": True,
        "DB_NAME": file.name
    })
    yield real_app

def test_set_key_value(client):
    response = client.post("/key_value?key=test_key&value=test_value")
    assert b"OK" in response.data

def test_fetch_key_value(client):
    client.post("/key_value?key=test_key&value=test_value")
    response = client.get("/key_value?key=test_key")
    assert b"test_value" in response.data

def test_submit_link(client):
    response = client.post("/save_url?url=" + urllib.parse.quote("http://google.com/"))
    assert b"OK" in response.data
