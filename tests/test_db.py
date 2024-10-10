from sqlalchemy import select

from fast_api_curso.models import User


def test_create_user(session):
    new_user = User(
        username="rafael",
        password="secret",
        email="teste@test",
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == "rafael"))

    assert user.username == "rafael"
