from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    semester = Column(String, nullable=False)

    topics = relationship("Topic", back_populates="subject", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="subject", cascade="all, delete-orphan")
    exams = relationship("Exam", back_populates="subject", cascade="all, delete-orphan")

class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    name = Column(String, nullable=False)
    difficulty = Column(Integer, default=3)  # 1 (Easy) to 5 (Hard)
    confidence = Column(Integer, default=3)  # 1 (Low) to 5 (High)

    subject = relationship("Subject", back_populates="topics")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    title = Column(String, nullable=False)
    deadline = Column(DateTime, nullable=False)
    estimated_minutes = Column(Integer, default=45)
    status = Column(String, default="pending")  # pending, completed, missed
    priority = Column(Integer, default=3)       # 1 (Low) to 5 (Urgent)

    subject = relationship("Subject", back_populates="tasks")

class Exam(Base):
    __tablename__ = "exams"
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    exam_date = Column(DateTime, nullable=False)
    syllabus_details = Column(String, default="")

    subject = relationship("Subject", back_populates="exams")

class StudyPreference(Base):
    __tablename__ = "study_preferences"
    id = Column(Integer, primary_key=True, index=True)
    daily_available_minutes = Column(Integer, default=180)
    preferred_session_length = Column(Integer, default=45)