import pytest
from fastapi.testclient import TestClient
from typing import  Generator
from adapters.src.repositories import Connection, SessionManager, SQLConnection
from api.src.create_app import create_app

@pytest.fixture(autouse=True)
def initialize_session() -> Generator[None, None, None]:
    connection: Connection = SQLConnection()
    SessionManager.initialize_session(connection)
    yield
    SessionManager.close_session()


@pytest.fixture
def api_client() -> TestClient:
    api = create_app()
    client = TestClient(api)

    return client
