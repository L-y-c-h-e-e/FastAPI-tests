from sqlalchemy.orm import Session
import models, schemas

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task_update: schemas.TaskBase):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        for key, value in task_update.model_dump().items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task

def get_tasks_sorted(db: Session, sort_by: str = "created_at", descending: bool = False):
    column = getattr(models.Task, sort_by, None)
    if column is None:
        column = models.Task.created_at
    if descending:
        return db.query(models.Task).order_by(column.desc()).all()
    return db.query(models.Task).order_by(column).all()

def get_top_priority_tasks(db: Session, limit: int = 5):
    return db.query(models.Task).order_by(models.Task.priority.desc()).limit(limit).all()

def search_tasks(db: Session, search_term: str):
    return db.query(models.Task).filter(
        (models.Task.title.contains(search_term)) |
        (models.Task.description.contains(search_term))).all()