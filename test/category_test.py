from fastapi import status

BASE_URL = "/api/v1/categories"

def test_create_category(test_client):
    response = test_client.post(BASE_URL, json={"name": "Test Category"})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "Test Category"

def test_get_categories(test_client):
    response = test_client.get(BASE_URL)
    assert response.status_code == status.HTTP_200_OK