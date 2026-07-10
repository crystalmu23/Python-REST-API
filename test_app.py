import pytest
from unittest.mock import patch
from app import app, inventory_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_inventory(client):
    res = client.get('/inventory')
    assert res.status_code == 200
    assert isinstance(res.json, list)

def test_create_item(client):
    payload = {"product_name": "Testing Oats", "price": 4.50}
    res = client.post('/inventory', json=payload)
    assert res.status_code == 201
    assert res.json["product_name"] == "Testing Oats"

def test_get_invalid_item(client):
    res = client.get('/inventory/99999')
    assert res.status_code == 404

def test_patch_item(client):
    res = client.patch('/inventory/1', json={"quantity": 100})
    assert res.status_code == 200
    assert res.json["quantity"] == 100

def test_delete_item(client):
    res = client.delete('/inventory/1')
    assert res.status_code == 200

@patch('app.requests.get')
def test_external_api_mock(mock_get, client):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Mock Premium Coffee",
            "brands": "Mock Beans",
            "ingredients_text": "Coffee beans"
        }
    }
    res = client.get('/api/external/fetch?barcode=12345678')
    assert res.status_code == 200
    assert res.json["product_name"] == "Mock Premium Coffee"
