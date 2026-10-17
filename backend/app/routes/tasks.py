from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Task
from app.schemas import TaskCreate, TaskOut

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", response_model=List[TaskOut])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

@router.post("/", response_model=TaskOut)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    task = Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.patch("/{task_id}/status")
def update_task_status(task_id: int, status: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = status
    db.commit()
    return {"message": "Task status updated", "status": task.status}