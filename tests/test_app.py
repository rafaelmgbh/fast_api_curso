from http import HTTPStatus


def test_read_root_return_succuses(client):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK


def test_read_html_return(client):
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


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "name": "johndoe",
            "password": "123456",
            "email": "jonh@test.com",
        },
    )
    assert response.status_code == HTTPStatus.CREATED


def test_read_users(client):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [{"id": 1, "name": "johndoe", "email": "jonh@test.com"}]
    }


def test_update_user(client):
    response = client.put(
        "/users/1",
        json={
            "name": "rafael",
            "email": "rafael@gmail.com",
            "password": "123456",
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "name": "rafael",
        "email": "rafael@gmail.com",
    }


def test_update_user_not_found(client):
    response = client.put(
        "/users/10",
        json={
            "name": "rafael",
            "email": "jose@gmail.com",
            "password": "123456",
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_read_user_by_id(client):
    response = client.get("/users/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "name": "rafael",
        "email": "rafael@gmail.com",
    }


def test_read_user_not_found(client):
    response = client.get("/users/10")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_delete_user(client):
    response = client.delete("/users/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"detail": "User deleted"}


def test_delete_user_not_found(client):
    response = client.delete("/users/10")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}
