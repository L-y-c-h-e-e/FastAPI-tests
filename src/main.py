from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, models
from src import CRUD
from src.database import engine
from dependencies import get_db

app = FastAPI()

# Создание таблиц (для первого запуска)
models.Base.metadata.create_all(bind=engine)

@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return CRUD.create_task(db, task)

@app.get("/tasks/", response_model=list[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return CRUD.get_tasks(db, skip=skip, limit=limit)

@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = CRUD.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskBase, db: Session = Depends(get_db)):
    db_task = CRUD.update_task(db, task_id=task_id, task_update=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.delete("/tasks/{task_id}", response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = CRUD.delete_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.get("/tasks/sorted/", response_model=list[schemas.Task])
def get_sorted_tasks(sort_by: str = "created_at", descending: bool = False, db: Session = Depends(get_db)):
    return CRUD.get_tasks_sorted(db, sort_by=sort_by, descending=descending)

@app.get("/tasks/top/", response_model=list[schemas.Task])
def get_top_tasks(limit: int = 5, db: Session = Depends(get_db)):
    return CRUD.get_top_priority_tasks(db, limit=limit)

@app.get("/tasks/search/", response_model=list[schemas.Task])
def search_tasks(search_term: str, db: Session = Depends(get_db)):
    return CRUD.search_tasks(db, search_term=search_term)