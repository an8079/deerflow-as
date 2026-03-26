"""
DeerFlow-X Projects & Tasks API
完整的 REST + WebSocket 端点实现
"""
import asyncio
import logging
import uuid
from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from pydantic import Field

from ..models.schemas import (
    ProjectCreate, ProjectResponse, ProjectUpdate, ProjectStatus,
    TaskCreate, TaskResponse, TaskUpdate, TaskStatus, AgentRole, TaskDispatch,
)
from ..core.in_memory_store import store
from ..agents.workflow import scheduler

logger = logging.getLogger(__name__)

# ─── 项目路由 ────────────────────────────────────────────────────────────────

projects_router = APIRouter(prefix="/projects", tags=["Projects"])


@projects_router.post("", response_model=ProjectResponse, status_code=201)
async def create_project(project: ProjectCreate):
    """创建新项目"""
    return store.create_project(name=project.name, description=project.description, goal=project.goal)


@projects_router.get("", response_model=List[ProjectResponse])
async def list_projects(status: Optional[ProjectStatus] = None):
    """列出所有项目"""
    return store.list_projects(status=status)


@projects_router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    """获取项目详情"""
    project = store.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@projects_router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: str, update: ProjectUpdate):
    """更新项目"""
    project = store.update_project(
        project_id,
        name=update.name,
        description=update.description,
        goal=update.goal,
        status=update.status,
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@projects_router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: str):
    """删除项目"""
    await scheduler.stop_project_workflow(project_id)
    if not store.delete_project(project_id):
        raise HTTPException(status_code=404, detail="Project not found")


@projects_router.post("/{project_id}/tasks", response_model=TaskResponse, status_code=201)
async def create_task(project_id: str, task: TaskCreate):
    """在项目中创建任务"""
    result = store.create_task(project_id, task)
    if not result:
        raise HTTPException(status_code=404, detail="Project not found")
    return result


@projects_router.get("/{project_id}/tasks", response_model=List[TaskResponse])
async def list_project_tasks(
    project_id: str,
    agent: Optional[AgentRole] = None,
    status: Optional[TaskStatus] = None,
):
    """列出项目的所有任务"""
    if not store.get_project(project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    return store.list_tasks(project_id=project_id, agent=agent, status=status)


@projects_router.get("/{project_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_project_task(project_id: str, task_id: str):
    """获取项目中指定任务"""
    task = store.get_task(task_id)
    if not task or task.project_id != project_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@projects_router.patch("/{project_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_project_task(project_id: str, task_id: str, update: TaskUpdate):
    """更新项目中指定任务"""
    task = store.get_task(task_id)
    if not task or task.project_id != project_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return store.update_task(
        task_id,
        status=update.status,
        result=update.result,
        error=update.error,
    )


@projects_router.delete("/{project_id}/tasks/{task_id}", status_code=204)
async def delete_project_task(project_id: str, task_id: str):
    """删除项目中指定任务"""
    task = store.get_task(task_id)
    if not task or task.project_id != project_id:
        raise HTTPException(status_code=404, detail="Task not found")
    store.delete_task(task_id)


@projects_router.post("/{project_id}/dispatch", status_code=202)
async def dispatch_task(project_id: str, dispatch: TaskDispatch):
    """派发任务给指定 Agent"""
    task = store.get_task(dispatch.task_id)
    if not task or task.project_id != project_id:
        raise HTTPException(status_code=404, detail="Task not found")
    success = store.dispatch_task(project_id, dispatch.task_id, dispatch.message)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to dispatch task")
    return {"status": "dispatched", "task_id": dispatch.task_id}


@projects_router.post("/{project_id}/start", status_code=202)
async def start_project_workflow(project_id: str, background_tasks: BackgroundTasks):
    """启动项目工作流"""
    project = store.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if scheduler.is_project_running(project_id):
        raise HTTPException(status_code=400, detail="Project workflow is already running")
    background_tasks.add_task(scheduler.start_project_workflow, project_id)
    return {"status": "started", "project_id": project_id}


@projects_router.post("/{project_id}/stop", status_code=200)
async def stop_project_workflow(project_id: str):
    """停止项目工作流"""
    success = await scheduler.stop_project_workflow(project_id)
    if not success:
        raise HTTPException(status_code=400, detail="Project workflow is not running")
    return {"status": "stopped", "project_id": project_id}


@projects_router.get("/{project_id}/status")
async def get_project_status(project_id: str):
    """获取项目状态摘要"""
    project = store.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    tasks = store.list_tasks(project_id=project_id)
    running = scheduler.is_project_running(project_id)
    workflow_state = scheduler.get_workflow_state(project_id)
    return {
        "project_id": project_id,
        "status": project.status.value,
        "is_running": running,
        "task_summary": {
            "total": len(tasks),
            "pending": len([t for t in tasks if t.status == TaskStatus.PENDING]),
            "running": len([t for t in tasks if t.status == TaskStatus.RUNNING]),
            "completed": len([t for t in tasks if t.status == TaskStatus.COMPLETED]),
            "failed": len([t for t in tasks if t.status == TaskStatus.FAILED]),
        },
        "workflow_step": workflow_state.get("step", 0) if workflow_state else 0,
    }


# ─── WebSocket 连接管理器 ──────────────────────────────────────────────────────

class ProjectConnectionManager:
    """管理项目 WebSocket 连接"""

    def __init__(self):
        # project_id -> set of websocket connections
        self._connections: dict[str, set[WebSocket]] = {}
        self._lock = asyncio.Lock()

    async def connect(self, project_id: str, websocket: WebSocket):
        await websocket.accept()
        async with self._lock:
            if project_id not in self._connections:
                self._connections[project_id] = set()
            self._connections[project_id].add(websocket)
        logger.info(f"[ws] Client connected to project {project_id}")

    async def disconnect(self, project_id: str, websocket: WebSocket):
        async with self._lock:
            if project_id in self._connections:
                self._connections[project_id].discard(websocket)
                if not self._connections[project_id]:
                    del self._connections[project_id]
        logger.info(f"[ws] Client disconnected from project {project_id}")

    async def broadcast(self, project_id: str, event: dict):
        """向项目所有订阅者广播事件"""
        async with self._lock:
            conns = set(self._connections.get(project_id, set()))
        if not conns:
            return
        dead = set()
        for ws in conns:
            try:
                await ws.send_json(event)
            except Exception:
                dead.add(ws)
        if dead:
            async with self._lock:
                for ws in dead:
                    if project_id in self._connections:
                        self._connections[project_id].discard(ws)


ws_manager = ProjectConnectionManager()


# ─── WebSocket 路由（独立路由，前缀为 /ws）──────────────────────────────────────

ws_router = APIRouter(prefix="/ws", tags=["WebSocket"])


@ws_router.websocket("/projects/{project_id}/events")
async def websocket_project_events(websocket: WebSocket, project_id: str):
    """WebSocket 端点：/ws/projects/{project_id}/events"""
    await ws_manager.connect(project_id, websocket)
    try:
        await ws_manager.broadcast(project_id, {
            "type": "connected",
            "project_id": project_id,
            "timestamp": datetime.utcnow().isoformat(),
        })
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        await ws_manager.disconnect(project_id, websocket)


# ─── 全局任务路由（不依赖 project_id）─────────────────────────────────────────

tasks_router = APIRouter(prefix="/tasks", tags=["Tasks"])


@tasks_router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """获取任务详情（全局）"""
    task = store.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@tasks_router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, update: TaskUpdate):
    """更新任务状态（全局）"""
    task = store.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return store.update_task(
        task_id,
        status=update.status,
        result=update.result,
        error=update.error,
    )


@tasks_router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: str):
    """删除任务（全局）"""
    task = store.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    store.delete_task(task_id)
