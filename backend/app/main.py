from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import subjects, tasks, exams, planner

Base.metadata.create_all(bind=engine)

app = FastAPI(title="StudyOS Core API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(subjects.router)
app.include_router(tasks.router)
app.include_router(exams.router)
app.include_router(planner.router)

@app.get("/")
def health_check():
    return {"status": "online", "system": "StudyOS Engine"}