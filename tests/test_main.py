from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_create_delete_client():
    """
    Request to create client
    Request to create client with existing username and email
    Request to delete client
    """
    payload = {
        "username": "client_test",
        "email": "client@pytest.com",
        "password": "test_pass"
    }
    response_new_create = client.post("/auth/clients/", json=payload)
    response_create_new_body = response_new_create.json()

    assert response_new_create.status_code == 201
    assert response_create_new_body["username"] == "client_test"
    assert response_create_new_body["email"] == "client@pytest.com"
    id = response_create_new_body["id"]

    response_create_existing = client.post("/auth/clients/", json=payload)

    assert response_create_existing.status_code == 400
    assert response_create_existing.text == '{"detail":"Email or username already exists."}'

    response_delete = client.delete(f"/auth/clients/{id}/")
    response_delete_body = response_delete.text

    assert response_delete.status_code == 200
    assert response_delete_body == '"Client client@pytest.com, was deleted."'

    response_bad_id_delete = client.delete(f"/auth/clients/99999/")
    assert response_bad_id_delete.status_code == 400
    assert response_bad_id_delete.text == '{"detail":"User does not exist."}'



def test_create_delete_managers():
    """
    Request to create new manager
    Request to create manager with existing username/email
    Request to delete manager
    Request to delete with not existing id
    """
    payload = {
        "username": "manager_test",
        "email": "manager@pytest.com",
        "password": "test_pass"
    }
    response_new_create = client.post("/auth/managers/signup/", json=payload)
    response_create_new_body = response_new_create.json()

    assert response_new_create.status_code == 201
    assert response_create_new_body["username"] == "manager_test"
    assert response_create_new_body["email"] == "manager@pytest.com"
    id = response_create_new_body["id"]

    response_create_existing = client.post("/auth/managers/signup/", json=payload)

    assert response_create_existing.status_code == 400
    assert response_create_existing.text == '{"detail":"Email or username already exists."}'

    response_delete = client.delete(f"/auth/managers/{id}/")
    response_delete_body = response_delete.text

    assert response_delete.status_code == 200
    assert response_delete_body == '"Manager manager@pytest.com was deleted."'

    response_bad_id_delete = client.delete(f"/auth/managers/99999/")
    assert response_bad_id_delete.status_code == 400
    assert response_bad_id_delete.text == '{"detail":"Manager does not exist."}'
