from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class TopicBase(BaseModel):
    name: str
    difficulty: int
    confidence: int

class TopicCreate(TopicBase):
    pass

class TopicOut(TopicBase):
    id: int
    subject_id: int
    class Config:
        from_attributes = True

class SubjectBase(BaseModel):
    name: str
    semester: str

class SubjectCreate(SubjectBase):
    pass

class SubjectOut(SubjectBase):
    id: int
    topics: List[TopicOut] = []
    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str
    deadline: datetime
    estimated_minutes: int
    priority: int
    status: Optional[str] = "pending"

class TaskCreate(TaskBase):
    subject_id: int

class TaskOut(TaskBase):
    id: int
    subject_id: int
    class Config:
        from_attributes = True

class ExamBase(BaseModel):
    exam_date: datetime
    syllabus_details: Optional[str] = ""

class ExamCreate(ExamBase):
    subject_id: int

class ExamOut(ExamBase):
    id: int
    subject_id: int
    class Config:
        from_attributes = True

class PlanItem(BaseModel):
    task_id: int
    title: str
    subject_name: str
    allocated_minutes: int
    urgency_score: float
    deadline: datetime
    reason: str

class PlanResponse(BaseModel):
    available_minutes: int
    total_allocated: int
    schedule: List[PlanItem]
    overflow_tasks: List[PlanItem]