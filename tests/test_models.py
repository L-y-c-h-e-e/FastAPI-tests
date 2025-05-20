from datetime import datetime, timezone
from src.models import Task


def test_task_model_creation():
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "status": "pending",
        "priority": 1
    }

    task = Task(**task_data)

    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.status == "pending"
    assert task.priority == 1
    assert isinstance(task.created_at, datetime)
    assert task.created_at.tzinfo == timezone.utc