"""
DeerFlow-X 数据模型定义
"""
import uuid
from datetime import datetime
from typing import Optional, List, Literal
from enum import Enum
from pydantic import BaseModel, Field


# ============== Agent 角色 ==============
class AgentRole(str, Enum):
    CEO = "ceo"           # 首席执行官：拆解目标、分配任务
    ARCHITECT = "architect"  # 架构师：技术方案设计
    PROGRAMMER = "programmer"  # 程序员：代码实现
    TESTER = "tester"     # 测试工程师：质量保障
    DEVOPS = "devops"     # 运维：部署与监控


# ============== 任务状态 ==============
class TaskStatus(str, Enum):
    PENDING = "pending"       # 等待中
    RUNNING = "running"       # 执行中
    COMPLETED = "completed"   # 已完成
    FAILED = "failed"         # 失败
    CANCELLED = "cancelled"   # 已取消


# ============== 项目状态 ==============
class ProjectStatus(str, Enum):
    ACTIVE = "active"         # 活跃
    PAUSED = "paused"         # 暂停
    COMPLETED = "completed"   # 已完成
    ARCHIVED = "archived"     # 已归档


# ============== 任务模型 ==============
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    assigned_agent: AgentRole
    priority: int = Field(default=0, ge=0, le=10)
    parent_task_id: Optional[str] = None


class TaskResponse(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str = ""
    assigned_agent: AgentRole
    status: TaskStatus = TaskStatus.PENDING
    priority: int = 0
    parent_task_id: Optional[str] = None
    project_id: str
    result: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class TaskUpdate(BaseModel):
    status: Optional[TaskStatus] = None
    result: Optional[str] = None
    error: Optional[str] = None


# ============== 项目模型 ==============
class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = ""
    goal: str = ""


class ProjectResponse(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str = ""
    goal: str = ""
    status: ProjectStatus = ProjectStatus.ACTIVE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    tasks: List[TaskResponse] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    goal: Optional[str] = None
    status: Optional[ProjectStatus] = None


# ============== 任务派发消息 ==============
class TaskDispatch(BaseModel):
    project_id: str
    task_id: str
    message: str = ""
    priority: int = 0


# ============== 团队成员 ==============
class TeamMember(BaseModel):
    role: AgentRole
    name: str
    is_active: bool = True
    current_task_id: Optional[str] = None


# ============== 项目团队 ==============
class ProjectTeam(BaseModel):
    project_id: str
    members: List[TeamMember] = Field(default_factory=list)
    ceo_id: Optional[str] = None
    architect_id: Optional[str] = None


# ============== LangGraph 状态 ==============
class GraphState(BaseModel):
    project_id: str
    current_task_id: Optional[str] = None
    task_history: List[str] = Field(default_factory=list)
    messages: List[dict] = Field(default_factory=list)
    context: dict = Field(default_factory=dict)
    step: int = 0
