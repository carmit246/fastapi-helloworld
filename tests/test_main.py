"""
Simple tests for FastAPI application
Run with: pytest tests/
"""
import os
import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    """Test the /one/hello endpoint"""
    response = client.get("/one/hello")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    # The response should contain HELLOWORLD_ENV key
    response_data = response.json()
    assert len(response_data) > 0


def test_read_root_with_env():
    """Test /one/hello endpoint with environment variable set"""
    # Set environment variable
    os.environ["HELLOWORLD_ENV"] = "test_environment"
    
    response = client.get("/one/hello")
    assert response.status_code == 200
    
    response_data = response.json()
    # Check that our env value is in the response
    assert "test_environment" in str(response_data)
    
    # Clean up
    del os.environ["HELLOWORLD_ENV"]


def test_read_root_without_env():
    """Test /one/hello when environment variable is not set"""
    # Ensure env var is not set
    if "HELLOWORLD_ENV" in os.environ:
        del os.environ["HELLOWORLD_ENV"]
    
    response = client.get("/one/hello")
    assert response.status_code == 200
    
    response_data = response.json()
    # Should contain "not found" message
    assert "not found" in str(response_data).lower()


def test_read_item():
    """Test the /items/{item_id} endpoint"""
    item_id = 42
    response = client.get(f"/items/{item_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["item_id"] == item_id
    assert "q" in data


def test_read_item_with_query():
    """Test /items endpoint with query parameter"""
    item_id = 100
    query_param = "test_query"
    
    response = client.get(f"/items/{item_id}?q={query_param}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["item_id"] == item_id
    assert data["q"] == query_param


def test_read_item_invalid_type():
    """Test /items with invalid item_id type"""
    response = client.get("/items/not_a_number")
    # FastAPI should return 422 for validation error
    assert response.status_code == 422


def test_get_api_key_without_file():
    """Test /get_api_key endpoint when config file doesn't exist"""
    response = client.get("/get_api_key")
    assert response.status_code == 200
    # Should return empty API key since file won't exist in test
    data = response.json()
    assert isinstance(data, dict)
    # The response should contain an API_KEY field
    assert "API_KEY" in data
    # API key should be empty string when file doesn't exist
    assert data["API_KEY"] == ""


def test_api_docs_available():
    """Test that API documentation is accessible"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_schema():
    """Test that OpenAPI schema is accessible"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "paths" in schema


def test_health_check_paths_exist():
    """Test that our defined paths exist in the app"""
    response = client.get("/openapi.json")
    schema = response.json()
    paths = schema["paths"]
    
    # Verify our endpoints are registered
    assert "/one/hello" in paths
    assert "/items/{item_id}" in paths
    assert "/get_api_key" in paths