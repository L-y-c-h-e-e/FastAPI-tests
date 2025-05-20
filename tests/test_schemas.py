from datetime import datetime
from src.schemas import TaskCreate, Task

def test_task_create_schema():
    task = TaskCreate(
        title="Test",
        description="Test desc",
        status="pending",
        priority=1
    )
    assert task.title == "Test"
    assert task.status == "pending"

def test_task_schema_with_datetime():
    task = Task(
        id=1,
        title="Test",
        description="Test desc",
        status="completed",
        priority=2,
        created_at=datetime.now()
    )
    assert task.id == 1
    assert task.status == "completed"