from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_api_curso.app import app

client = TestClient(app)


def test_read_root_return_succuses():
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK


def test_read_root_return_html():
    response = client.get("/html")
    assert response.status_code == HTTPStatus.OK
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert (
        response.text
        == """
    <html>
        <head>
            <title>Este e o Retorno da Requisição</title>
        </head>
        <body>
            <h1>Olá Mundo</h1>
        </body>
    """
    )
