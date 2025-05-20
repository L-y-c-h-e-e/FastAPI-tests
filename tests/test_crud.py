from sqlalchemy.orm import Session
from src.models import Task
from src.schemas import TaskCreate
from src.CRUD import create_task, get_task, update_task, delete_task, get_tasks_sorted, get_top_priority_tasks, search_tasks


def test_create_task(db_session: Session):
    task_data = TaskCreate(
        title="Test Task",
        description="Test Description",
        status="pending",
        priority=1
    )

    task = create_task(db_session, task_data)
    assert task.id is not None
    assert db_session.query(Task).count() == 1


def test_get_task(db_session: Session):
    db_task = Task(
        title="Test Task",
        description="Test Description",
        status="pending",
        priority=1
    )
    db_session.add(db_task)
    db_session.commit()

    retrieved_task = get_task(db_session, db_task.id)
    assert retrieved_task.id == db_task.id


def test_update_task(db_session: Session):
    db_task = Task(
        title="Original Title",
        description="Original Desc",
        status="pending",
        priority=1
    )
    db_session.add(db_task)
    db_session.commit()

    updated_data = TaskCreate(
        title="Updated Title",
        description="Updated Desc",
        status="in_progress",
        priority=2
    )

    updated_task = update_task(db_session, db_task.id, updated_data)
    assert updated_task.title == "Updated Title"
    assert updated_task.status == "in_progress"


def test_task_statuses(db_session: Session):
    for status in ["pending", "in_progress", "completed"]:
        task = Task(title=f"Task {status}", status=status)
        db_session.add(task)
    db_session.commit()

    assert db_session.query(Task).count() == 3


def test_delete_task(db_session: Session):
    task = Task(title="To be deleted", description="Delete me")
    db_session.add(task)
    db_session.commit()

    deleted_task = delete_task(db_session, task.id)
    assert deleted_task.id == task.id
    assert db_session.query(Task).count() == 0


def test_get_tasks_sorted(db_session: Session):
    tasks = [
        Task(title="Task 1", priority=3),
        Task(title="Task 2", priority=1),
        Task(title="Task 3", priority=2)
    ]
    db_session.add_all(tasks)
    db_session.commit()

    sorted_tasks = get_tasks_sorted(db_session, sort_by="priority")
    assert [t.priority for t in sorted_tasks] == [1, 2, 3]


def test_get_top_priority_tasks(db_session: Session):
    tasks = [
        Task(title="Low", priority=1),
        Task(title="High", priority=3),
        Task(title="Medium", priority=2)
    ]
    db_session.add_all(tasks)
    db_session.commit()

    top_tasks = get_top_priority_tasks(db_session, limit=2)
    assert len(top_tasks) == 2
    assert top_tasks[0].priority == 3
    assert top_tasks[1].priority == 2


def test_search_tasks(db_session: Session):
    tasks = [
        Task(title="Find me", description="Important"),
        Task(title="Another", description="Not me")
    ]
    db_session.add_all(tasks)
    db_session.commit()

    results = search_tasks(db_session, "Find")
    assert len(results) == 1
    assert results[0].title == "Find me"