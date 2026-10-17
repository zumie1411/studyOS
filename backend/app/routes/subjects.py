from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Subject, Topic
from app.schemas import SubjectCreate, SubjectOut, TopicCreate, TopicOut

router = APIRouter(prefix="/subjects", tags=["Subjects"])

@router.get("/", response_model=List[SubjectOut])
def get_subjects(db: Session = Depends(get_db)):
    return db.query(Subject).all()

@router.post("/", response_model=SubjectOut)
def create_subject(payload: SubjectCreate, db: Session = Depends(get_db)):
    subject = Subject(**payload.model_dump())
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject

@router.post("/{subject_id}/topics", response_model=TopicOut)
def add_topic(subject_id: int, payload: TopicCreate, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    topic = Topic(**payload.model_dump(), subject_id=subject_id)
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic