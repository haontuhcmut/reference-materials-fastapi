from fastapi import status
from app.config import Config

BASE_URL = f"{Config.VERSION}/category"

def test_create_category(test_client):
    response = test_client.post(f"{BASE_URL}/", json={"name": "bio"})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "bio"

    category_id = response.json()["id"]

    response = test_client.get(f"{BASE_URL}/{category_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == str(category_id)
    assert response.json()["name"] == "bio"

