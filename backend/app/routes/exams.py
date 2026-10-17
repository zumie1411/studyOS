from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Exam
from app.schemas import ExamCreate, ExamOut

router = APIRouter(prefix="/exams", tags=["Exams"])

@router.get("/", response_model=List[ExamOut])
def get_exams(db: Session = Depends(get_db)):
    return db.query(Exam).order_by(Exam.exam_date.asc()).all()

@router.post("/", response_model=ExamOut)
def create_exam(payload: ExamCreate, db: Session = Depends(get_db)):
    exam = Exam(**payload.model_dump())
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam