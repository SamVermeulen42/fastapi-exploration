from fastapi import HTTPException, Security, FastAPI
from starlette.testclient import TestClient

from app.api import get_api_key
from app.main import app


fake_api_key = "123"
fake_db = {
    "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
    "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
}

client = TestClient(app)


async def override_api_key():
    return 'test'

app.dependency_overrides[get_api_key] = override_api_key

def test_read_main():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response == "pong"


