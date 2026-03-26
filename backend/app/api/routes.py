"""DeerFlow-X API Routes"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime

router = APIRouter()
TASK_STORE = {}

class TaskCreate(BaseModel):
    task: str
    context: Optional[dict] = None
    workflow_id: Optional[str] = None

class TaskStatus(BaseModel):
    task_id: str
    status: str
    current_agent: Optional[str] = None
    progress: float = 0.0
    result: Optional[dict] = None
    errors: List[str] = []
    created_at: str

@router.post("/tasks", response_model=TaskStatus)
async def create_task(req: TaskCreate):
    task_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    TASK_STORE[task_id] = {
        "task_id": task_id, "status": "queued",
        "current_agent": None, "progress": 0.0,
        "result": None, "errors": [],
        "created_at": now, "updated_at": now
    }
    return TASK_STORE[task_id]

@router.get("/tasks/{task_id}", response_model=TaskStatus)
async def get_task(task_id: str):
    if task_id not in TASK_STORE:
        raise HTTPException(status_code=404, detail="Task not found")
    return TASK_STORE[task_id]

@router.get("/tasks", response_model=List[TaskStatus])
async def list_tasks(limit: int = 20):
    tasks = sorted(TASK_STORE.values(), key=lambda t: t["created_at"], reverse=True)
    return tasks[:limit]