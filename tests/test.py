from fastapi.testclient import TestClient
from main import app
from db import Base, test_engine
import pytest
import os


# Override app dependency to use test database session
# app.dependency_overrides[get_db] = lambda: TestSessionLocal()


@pytest.fixture(scope="session", autouse=True)
def set_unit_testing_env():
    os.environ["UNIT_TESTING"] = "1"  # Set UNIT_TESTING to indicate unit testing
    yield
    del os.environ["UNIT_TESTING"]  # Clean up environment variable after tests
    
    
@pytest.fixture(scope="module", autouse=True)
def setup_test_database():
    Base.metadata.create_all(bind=test_engine)  # Create tables in test database
    yield  # Run the test function
    Base.metadata.drop_all(bind=test_engine) 


client = TestClient(app)


# Test cases for create_address API
def test_create_address():
    address_data = {
        "street": "123 Main St",
        "city": "New York",
        "state": "NY",
        "postal_code": 100016,
        "latitude": 40.7128,
        "longitude": -74.0060
    }
    response = client.post("/addresses/", json=address_data)
    assert response.status_code == 200
    assert response.json().get("id") is not None

# # Test cases for read_address API
def test_read_address():
    # Assuming address_id 1 exists in the database
    response = client.get("/addresses/1")
    assert response.status_code == 200
    assert response.json() is not None

    # Assuming address_id 999 does not exist in the database
    response = client.get("/addresses/999")
    assert response.status_code == 404

# # Test cases for update_address API
def test_update_address():
    # Assuming address_id 1 exists in the database
    address_data = {
        "city": "Updated City"
    }
    response = client.put("/addresses/1", json=address_data)
    assert response.status_code == 200
    assert response.json().get("city") == "Updated City"

    # Assuming address_id 999 does not exist in the database
    response = client.put("/addresses/999", json=address_data)
    assert response.status_code == 404

# Test cases for delete_address API
def test_delete_address():
    # Assuming address_id 1 exists in the database
    response = client.delete("/addresses/1")
    assert response.status_code == 200
    
    # Assuming address_id 999 does not exist in the database
    response = client.delete("/addresses/999")
    assert response.status_code == 404