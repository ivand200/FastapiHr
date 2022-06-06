from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_clients():
    """
    Request to add tags to client
    Request to delete tags from client
    Request to get client with all tags
    """
    payload = {
        "tags_id": [
            5,
            2,
            1
        ]
    }
    # Add tags to client
    request_to_add = client.post("clients/client/1", json=payload)
    request_to_add_body = request_to_add.json()
    assert request_to_add.status_code == 201
    assert request_to_add_body["user"]["id"] == 1
    assert len(request_to_add_body["tags"]) > 2

    # Delete tags from client
    request_to_delete = client.delete("clients/client/1", json=payload)
    assert request_to_delete.status_code == 204

    #Get client by id with all tags
    request_get_client = client.get("clients/client/1")
    request_get_client_body = request_get_client.json()
    assert request_get_client.status_code == 200
    assert request_get_client_body["user"]["id"] == 1
    assert len(request_get_client_body["tags"]) > 1
