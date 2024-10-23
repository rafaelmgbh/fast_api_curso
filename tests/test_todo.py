from http import HTTPStatus

import factory.fuzzy

from fast_api_curso.models import Todo, TodoState


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker("text")
    description = factory.Faker("text")
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1


def test_create_todo(client, token, mock_db_time):
    with mock_db_time(model=Todo) as time:
        response = client.post(
            "/todos/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "title": "Test todo",
                "description": "Test todo description",
                "state": "draft",
            },
        )

    assert response.json() == {
        "id": 1,
        "title": "Test todo",
        "description": "Test todo description",
        "state": "draft",
        "created_at": time.isoformat(),
        "updated_at": time.isoformat(),
    }


def test_list_todos_should_return_all_expected_fields__exercicio(
    session, client, user, token, mock_db_time
):
    with mock_db_time(model=Todo) as time:
        todo = TodoFactory.create(user_id=user.id)
        session.add(todo)
        session.commit()

    session.refresh(todo)
    response = client.get(
        "/todos/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.json()["todos"] == [
        {
            "created_at": time.isoformat(),
            "updated_at": time.isoformat(),
            "description": todo.description,
            "id": todo.id,
            "state": todo.state,
            "title": todo.title,
        }
    ]


def test_patch_todo_error(client, token):
    response = client.patch(
        "/todos/10",
        json={},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Task not found."}


def test_patch_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.patch(
        f"/todos/{todo.id}",
        json={"title": "teste!"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["title"] == "teste!"


def test_delete_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.delete(
        f"/todos/{todo.id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "message": "Task has been deleted successfully."
    }


def test_delete_todo_error(client, token):
    response = client.delete(
        f"/todos/{10}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Task not found."}
