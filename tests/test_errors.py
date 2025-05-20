from fastapi import status

def test_create_task_invalid_data(client):
    response = client.post(
        "/tasks/",
        json={
            "title": "",
            "description": "Test",
            "status": "invalid_status",
            "priority": 0
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_data = response.json()
    assert any(error["type"] == "enum" for error in response_data["detail"])
    assert any(error["type"] == "value_error" for error in response_data["detail"])