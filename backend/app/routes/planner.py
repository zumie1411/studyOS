from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import PlanResponse
from app.services.scheduler import generate_study_plan

router = APIRouter(prefix="/planner", tags=["Planner"])

@router.get("/today", response_model=PlanResponse)
def get_today_plan(
    available_minutes: int = Query(180, description="Available study time in minutes"),
    recovery: bool = Query(False, description="Enable recovery replanner"),
    db: Session = Depends(get_db)
):
    return generate_study_plan(db, available_minutes=available_minutes, recovery_mode=recovery)