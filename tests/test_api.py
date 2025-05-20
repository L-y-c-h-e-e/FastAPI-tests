from fastapi import status


def test_create_task(client):
    response = client.post(
        "/tasks/",
        json={
            "title": "API Test Task",
            "description": "Test Description",
            "status": "pending",
            "priority": 1
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "API Test Task"
    assert "id" in data


def test_get_task(client):
    create_response = client.post(
        "/tasks/",
        json={
            "title": "Test Get Task",
            "description": "For GET test",
            "status": "pending",
            "priority": 1
        }
    )
    task_id = create_response.json()["id"]

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json()["title"] == "Test Get Task"


def test_update_nonexistent_task(client):
    response = client.put("/tasks/999", json={"title": "New Title"})
    assert response.status_code == 404


def test_delete_task(client):
    create_resp = client.post("/tasks/", json={"title": "To delete"})
    task_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/tasks/{task_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json()["id"] == task_id

    get_resp = client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 404


def test_get_sorted_tasks(client):
    client.post("/tasks/", json={"title": "Task 1", "priority": 2})
    client.post("/tasks/", json={"title": "Task 2", "priority": 1})

    response = client.get("/tasks/sorted/?sort_by=priority")
    assert response.status_code == 200
    tasks = response.json()
    assert tasks[0]["priority"] == 1
    assert tasks[1]["priority"] == 2


def test_get_top_tasks(client):
    client.post("/tasks/", json={"title": "Low", "priority": 1})
    client.post("/tasks/", json={"title": "High", "priority": 3})

    response = client.get("/tasks/top/?limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["priority"] == 3


def test_search_tasks(client):
    client.post("/tasks/", json={"title": "Important task", "description": "Find me"})

    response = client.get("/tasks/search/?search_term=Important")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert "Important" in response.json()[0]["title"]