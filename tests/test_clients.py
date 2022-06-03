from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_create_delete_fields():
    """
    Request to create field
    Request to create existing field
    Request to delete field
    Request to delete non existing field
    """
    payload = {
        "title": "jogging"
    }

    request_create_field = client.post("clients/fields/", json=payload)
    request_create_field_body = request_create_field.json()
    assert request_create_field.status_code == 201
    assert request_create_field_body["title"] == "jogging"
    id = request_create_field_body["id"]

    request_create_existing_field = client.post("clients/fields/", json=payload)
    request_create_existing_field_body = request_create_existing_field.json()
    assert request_create_existing_field.status_code == 400

    request_delete_field = client.delete(f"clients/fields/{id}/")
    assert request_delete_field.status_code == 204

    request_delete_fake_field = client.delete("clients/fields/9999/")
    assert request_delete_fake_field.status_code == 400
