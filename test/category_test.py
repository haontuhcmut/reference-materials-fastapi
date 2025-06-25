from fastapi import status
from app.main import app
import pytest

BASE_URL = "api/v1/category"

# Test data
category_data = dict(name="test")
update_category_data = dict(name="test")
invalid_uuid = "2619D907"  # Invalid UUID format
non_existent_uuid = "2619D907-AD69-43D0-89E5-D45EADF6F94B"  # Non-existent UUID


# Success cases
@pytest.mark.asyncio
async def test_create_get_category(async_client):
    """Test successful category creation and retrieval"""
    # Create category
    response = await async_client.post(f"{BASE_URL}/", json=category_data)
    assert response.status_code == 201
    assert response.json()["name"] == category_data["name"]

    # Get created category
    category_id = response.json()["id"]
    response = await async_client.get(f"{BASE_URL}/{category_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == str(category_id)
    assert response.json()["name"] == category_data["name"]

    # Update category
    response = await async_client.put(
        f"{BASE_URL}/{category_id}", json=update_category_data
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == update_category_data["name"]

    # Delete category
    response = await async_client.delete(f"{BASE_URL}/{category_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "The category is deleted successfully"}


@pytest.mark.asyncio
async def test_get_all_categories(async_client):
    """Test successful retrieval of all categories with pagination"""
    # Test pagination
    response = await async_client.get(f"{BASE_URL}/", params={"page": 1, "size": 10})
    assert response.status_code == status.HTTP_200_OK

    # Verify pagination response structure
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data
    assert "pages" in data
    assert isinstance(data["items"], list)
    assert data["page"] == 1
    assert data["size"] == 10


@pytest.mark.asyncio
async def test_order_by(async_client):
    response = await async_client.get(f"{BASE_URL}/", params={"order_by": "-name"})
    assert response.status_code == status.HTTP_200_OK


# Error cases - Create
@pytest.mark.asyncio
async def test_create_category_duplicate(async_client):
    """Test error when creating category with dupicate name"""
    # Create a new category
    response = await async_client.post(f"{BASE_URL}/", json=category_data)
    assert response.status_code == status.HTTP_201_CREATED

    # Try to create duplicate
    response = await async_client.post(f"{BASE_URL}/", json=category_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "message": "Category name already exist",
        "error_code": "category_name_already_exist",
    }


@pytest.mark.asyncio
async def test_cretegory_invalid_payload(async_client):
    """Test error when creating category with invalid payload"""
    response = await async_client.post(f"{BASE_URL}/", json=[])
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert (
        response.json()["detail"][0]["msg"]
        == "Input should be a valid dictionary or object to extract fields from"
    )


# Error cases - Read
@pytest.mark.asyncio
async def test_get_category_invalid_uuid(async_client):
    """Test error when getting category with invalid UUID format"""
    response = await async_client.get(f"{BASE_URL}/{invalid_uuid}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "message": "Invalid ID format",
        "error_code": "invalid_id_format",
    }


@pytest.mark.asyncio
async def test_get_category_not_found(async_client):
    """Assuming a category id '2619D907-AD69-43D0-89E5-D45EADF6F94B' does not exist"""
    response = await async_client.get(f"{BASE_URL}/{non_existent_uuid}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "message": "Category not found",
        "error_code": "category_not_found",
    }


@pytest.mark.asyncio
async def test_get_all_categories_invalid_pagination(async_client):
    """Test errpr when getting categories with invalid pagination parameter"""
    # Test invalid page number
    response = await async_client.get(f"{BASE_URL}/", params={"page": 0, "size": 10})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Test invalid page size
    response = await async_client.get(f"{BASE_URL}/", params={"page": 1, "size": 0})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Test negative value
    response = await async_client.get(f"{BASE_URL}/", params={"page": -1, "size": -10})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

# Error cases - Update
@pytest.mark.asyncio
async def test_update_category_invalid_uuid(async_client):
    """Test error when choosing category with invalid UUID format"""
    response = await async_client.put(
        f"{BASE_URL}/{invalid_uuid}", json=update_category_data
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "message": "Invalid ID format",
        "error_code": "invalid_id_format",
    }


@pytest.mark.asyncio
async def test_update_category_not_found(async_client):
    response = await async_client.put(
        f"{BASE_URL}/{non_existent_uuid}", json=update_category_data
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "message": "Category not found",
        "error_code": "category_not_found",
    }


@pytest.mark.asyncio
async def test_update_category_exist(async_client):
    response = await async_client.post(f"{BASE_URL}/", json={"name": "draft"})
    assert response.status_code == status.HTTP_201_CREATED

    category_id = response.json()["id"]
    response = await async_client.put(f"{BASE_URL}/{category_id}", json=category_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "message": "Category name already exist",
        "error_code": "category_name_already_exist",
    }


# Error cases - Delete
@pytest.mark.asyncio
async def test_delete_category_invalid_uuid(async_client):
    response = await async_client.delete(f"{BASE_URL}/{invalid_uuid}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "message": "Invalid ID format",
        "error_code": "invalid_id_format",
    }


@pytest.mark.asyncio
async def test_delete_category_not_found(async_client):
    response = await async_client.delete(f"{BASE_URL}/{non_existent_uuid}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "message": "Category not found",
        "error_code": "category_not_found",
    }
