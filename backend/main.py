# DeerFlow-X Backend — SoloPreneurs OS Core
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="DeerFlow-X API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TaskRequest(BaseModel):
    task: str
    context: dict | None = None


class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: dict | None = None


@app.get("/health")
async def health():
    return {"status": "alive", "service": "deer-flow-x", "version": "0.1.0"}


@app.post("/tasks", response_model=TaskResponse)
async def create_task(req: TaskRequest):
    # TODO: Integrate LangGraph workflow
    return TaskResponse(
        task_id="placeholder-id",
        status="queued",
        result={"message": "Task queued. LangGraph workflow coming soon."}
    )


@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    return TaskResponse(
        task_id=task_id,
        status="pending",
        result=None
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
