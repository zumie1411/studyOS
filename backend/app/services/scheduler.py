from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from app.models import Task, Exam, Topic, Subject

def calculate_priority_score(task: Task, db: Session) -> float:
    now = datetime.now()
    time_diff_hours = (task.deadline - now).total_seconds() / 3600.0

    # 1. Urgency multiplier (closer deadline = higher score)
    if time_diff_hours <= 0:
        urgency = 10.0  # Already overdue
    elif time_diff_hours <= 24:
        urgency = 8.0
    elif time_diff_hours <= 72:
        urgency = 5.0
    else:
        urgency = max(1.0, 10.0 - (time_diff_hours / 24.0))

    # 2. Upcoming Exam factor for the same subject
    nearest_exam = db.query(Exam).filter(
        Exam.subject_id == task.subject_id,
        Exam.exam_date >= now
    ).order_by(Exam.exam_date.asc()).first()

    exam_boost = 0.0
    if nearest_exam:
        days_to_exam = (nearest_exam.exam_date - now).total_seconds() / 86400.0
        if days_to_exam < 7:
            exam_boost = 4.0

    # 3. Topic weakness factor
    topics = db.query(Topic).filter(Topic.subject_id == task.subject_id).all()
    avg_gap = 0.0
    if topics:
        avg_gap = sum((t.difficulty - t.confidence) for t in topics) / len(topics)

    total_score = (task.priority * 2.0) + urgency + exam_boost + max(0.0, avg_gap)
    return round(total_score, 2)

def generate_study_plan(db: Session, available_minutes: int, recovery_mode: bool = False):
    tasks_query = db.query(Task).filter(Task.status.in_(["pending", "missed"]))
    tasks = tasks_query.all()

    scored_items = []
    for t in tasks:
        score = calculate_priority_score(t, db)
        if recovery_mode and t.status == "missed":
            score += 5.0  # Recovery boost for missed tasks

        subj = db.query(Subject).filter(Subject.id == t.subject_id).first()
        subj_name = subj.name if subj else "Unknown"

        reason = "Normal scheduled work"
        if t.status == "missed":
            reason = "Recovery: Missed session prioritised"
        elif (t.deadline - datetime.now()).total_seconds() / 3600.0 < 24:
            reason = "High urgency: Due within 24h"

        scored_items.append({
            "task_id": t.id,
            "title": t.title,
            "subject_name": subj_name,
            "allocated_minutes": t.estimated_minutes,
            "urgency_score": score,
            "deadline": t.deadline,
            "reason": reason
        })

    # Sort descending by calculated priority score
    scored_items.sort(key=lambda x: x["urgency_score"], reverse=True)

    schedule = []
    overflow = []
    used_time = 0

    for item in scored_items:
        if used_time + item["allocated_minutes"] <= available_minutes:
            schedule.append(item)
            used_time += item["allocated_minutes"]
        else:
            overflow.append(item)

    return {
        "available_minutes": available_minutes,
        "total_allocated": used_time,
        "schedule": schedule,
        "overflow_tasks": overflow
    }