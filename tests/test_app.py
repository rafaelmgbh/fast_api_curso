from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_api_curso.app import app

client = TestClient(app)


def test_read_root_return_succuses():
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
