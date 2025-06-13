from fastapi import status
from app.main import app
import pytest

BASE_URL = "api/v1/category"


@pytest.mark.asyncio
async def test_create_category(async_client):
    response = await async_client.post(f"{BASE_URL}/", json={"name": "test"})

    assert response.status_code == 201
    assert response.json()["name"] == "test"

