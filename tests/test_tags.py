from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_create_delete_fields():
    """
    Request to create field
    Request to create existing field
    Request to delete field
    Request to delete non existing field
    Update field
    Get all fields
    """
    payload = {
        "title": "jogging"
    }

    payload_update = {
        "title": "running"
    }
    # Create field
    request_create_field = client.post("tags/fields", json=payload)
    request_create_field_body = request_create_field.json()
    assert request_create_field.status_code == 201
    assert request_create_field_body["title"] == "jogging"
    id = request_create_field_body["id"]

    # Create existing field
    request_create_existing_field = client.post("tags/fields", json=payload)
    request_create_existing_field_body = request_create_existing_field.json()
    assert request_create_existing_field.status_code == 400

    # Update field
    request_to_update = client.put(f"tags/fields/{id}", json=payload_update)
    request_to_update_body = request_to_update.json()
    assert request_to_update.status_code == 200
    assert request_to_update_body["title"] == "running"

    # Delete field
    request_delete_field = client.delete(f"tags/fields/{id}")
    assert request_delete_field.status_code == 204

    # Delete fake field
    request_delete_fake_field = client.delete("tags/fields/9999")
    assert request_delete_fake_field.status_code == 400

    # Get all fields
    request_all_fields = client.get("tags/fields")
    request_all_fields_body = request_all_fields.json()
    assert request_all_fields.status_code == 200
    assert len(request_all_fields_body) > 1


def test_tags():
    """
    Request to create tag
    Request to create existing tag
    Request delete tag
    Request get all tags
    """
    payload = {
        "title": "time traveling",
        "field_id": 3
    }
    # Create a new tag
    request_to_create = client.post("tags/tag", json=payload)
    request_to_create_body = request_to_create.json()
    assert request_to_create.status_code == 201
    assert request_to_create_body["title"] == "time traveling"
    assert request_to_create_body["field_id"] == 3
    id = request_to_create_body["id"]

    # Create tag with existing title
    request_to_create_existing = client.post("tags/tag", json=payload)
    assert request_to_create_existing.status_code == 400

    # Delete tag by id
    request_to_delete = client.delete(f"/tags/tag/{id}")
    assert request_to_delete.status_code == 204

    # Get all tags
    request_all_tags = client.get("tags/tag")
    request_all_tags_body = request_all_tags.json()
    assert request_all_tags.status_code == 200
    assert len(request_all_tags_body) > 2
