import pytest
from httpx import AsyncClient
from main import app
from fastapi import status


@pytest.mark.asyncio
async def test_read_root():
    """Test the root endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"Hello": "World"}


@pytest.mark.asyncio
async def test_read_item():
    """Test the read_item endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/items/1?q=test_query")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"item_id": 1, "q": "test_query"}


@pytest.mark.asyncio
async def test_update_item():
    """Test the update_item endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {"name": "Test Item", "description": "A test item", "price": 10.0}
        response = await client.put("/items/1", json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"item_name": "Test Item", "item_id": 1}