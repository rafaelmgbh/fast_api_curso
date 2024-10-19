from http import HTTPStatus

from fast_api_curso.schemas import UserPublic


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
            "username": "johndoe",
            "password": "123456",
            "email": "jonh@test.com",
        },
    )
    assert response.status_code == HTTPStatus.CREATED


def test_create_user_email_exists(client, user):
    response = client.post(
        "/users/",
        json={
            "username": "johndoe",
            "password": "123456",
            "email": "teste@test.com",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Email already exists"}


def test_create_user_username_exists(client, user):
    response = client.post(
        "/users/",
        json={
            "username": "rafael",
            "password": "123456",
            "email": "zeze@gmail.com",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Username already exists"}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


def test_read_users(client):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_update_user(client, user, token):
    response = client.put(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "rafael",
            "email": "rafael@gmail.com",
            "password": "123456",
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": user.id,
        "username": "rafael",
        "email": "rafael@gmail.com",
    }


def test_read_user_by_id(client, user):
    response = client.get("/users/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": "rafael",
        "email": "teste@test.com",
    }


def test_read_user_not_found(client):
    response = client.get("/users/10")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_delete_user(client, user, token):
    response = client.delete(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def test_get_token(client, user):
    response = client.post(
        "/token",
        data={"username": user.email, "password": user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in token
    assert "token_type" in token
