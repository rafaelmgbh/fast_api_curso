import pytest
from starlette.testclient import TestClient

from fast_api_curso.app import app


@pytest.fixture
def client():
    return TestClient(app)
