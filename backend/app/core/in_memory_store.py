"""
内存数据存储（支持 Redis 扩展）
用于多项目并发管理的内存数据库
"""
import asyncio
import uuid
import threading
from datetime import datetime
from typing import Dict, Optional, List
from collections import defaultdict
from dataclasses import dataclass, field
import logging

from ..models.schemas import (
    ProjectResponse, ProjectStatus, TaskResponse, TaskStatus,
    AgentRole, TaskCreate, TeamMember, ProjectTeam, GraphState
)

logger = logging.getLogger(__name__)


@dataclass
class InMemoryStore:
    """线程安全的内存存储"""
    
    # 存储
    projects: Dict[str, ProjectResponse] = field(default_factory=dict)
    tasks: Dict[str, TaskResponse] = field(default_factory=dict)
    teams: Dict[str, ProjectTeam] = field(default_factory=dict)
    graph_states: Dict[str, GraphState] = field(default_factory=dict)
    
    # 锁
    _lock: threading.Lock = field(default_factory=threading.Lock)
    
    # 队列
    pending_tasks: Dict[AgentRole, List[str]] = field(
        default_factory=lambda: defaultdict(list)
    )
    
    # ============== 项目操作 ==============
    
    def create_project(self, name: str, description: str = "", goal: str = "") -> ProjectResponse:
        """创建新项目"""
        with self._lock:
            project_id = str(uuid.uuid4())
            project = ProjectResponse(
                id=project_id,
                name=name,
                description=description,
                goal=goal,
                status=ProjectStatus.ACTIVE,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            self.projects[project_id] = project
            
            # 初始化项目团队
            self.teams[project_id] = ProjectTeam(
                project_id=project_id,
                members=[
                    TeamMember(role=AgentRole.CEO, name="CEO Agent"),
                    TeamMember(role=AgentRole.ARCHITECT, name="Architect Agent"),
                    TeamMember(role=AgentRole.PROGRAMMER, name="Programmer Agent"),
                    TeamMember(role=AgentRole.TESTER, name="Tester Agent"),
                    TeamMember(role=AgentRole.DEVOPS, name="DevOps Agent"),
                ]
            )
            
            # 初始化 LangGraph 状态
            self.graph_states[project_id] = GraphState(project_id=project_id)
            
            logger.info(f"Created project: {project_id} ({name})")
            return project
    
    def get_project(self, project_id: str) -> Optional[ProjectResponse]:
        """获取项目"""
        return self.projects.get(project_id)
    
    def list_projects(self, status: Optional[ProjectStatus] = None) -> List[ProjectResponse]:
        """列出所有项目"""
        with self._lock:
            projects = list(self.projects.values())
            if status:
                projects = [p for p in projects if p.status == status]
            return sorted(projects, key=lambda x: x.updated_at, reverse=True)
    
    def update_project(self, project_id: str, **kwargs) -> Optional[ProjectResponse]:
        """更新项目"""
        with self._lock:
            project = self.projects.get(project_id)
            if not project:
                return None
            for key, value in kwargs.items():
                if value is not None and hasattr(project, key):
                    setattr(project, key, value)
            project.updated_at = datetime.utcnow()
            return project
    
    def delete_project(self, project_id: str) -> bool:
        """删除项目及其所有任务"""
        with self._lock:
            if project_id not in self.projects:
                return False
            # 删除所有关联任务
            task_ids = [t.id for t in self.tasks.values() if t.project_id == project_id]
            for task_id in task_ids:
                del self.tasks[task_id]
            # 清理团队、图状态
            self.teams.pop(project_id, None)
            self.graph_states.pop(project_id, None)
            # 清理队列：只移除属于此项目的任务
            for role_tasks in self.pending_tasks.values():
                role_tasks[:] = [
                    t for t in role_tasks
                    if t not in self.tasks or self.tasks[t].project_id != project_id
                ]
            # 删除项目
            del self.projects[project_id]
            logger.info(f"Deleted project: {project_id}")
            return True
    
    # ============== 任务操作 ==============
    
    def create_task(self, project_id: str, task: TaskCreate) -> Optional[TaskResponse]:
        """创建任务"""
        with self._lock:
            if project_id not in self.projects:
                return None
            
            task_id = str(uuid.uuid4())
            task_response = TaskResponse(
                id=task_id,
                title=task.title,
                description=task.description,
                assigned_agent=task.assigned_agent,
                priority=task.priority,
                parent_task_id=task.parent_task_id,
                project_id=project_id,
                status=TaskStatus.PENDING,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            self.tasks[task_id] = task_response
            
            # 加入对应角色的待办队列
            self.pending_tasks[task.assigned_agent].append(task_id)
            
            # 更新项目任务列表
            self.projects[project_id].tasks.append(task_response)
            self.projects[project_id].updated_at = datetime.utcnow()
            
            logger.info(f"Created task: {task_id} for project {project_id}")
            return task_response
    
    def get_task(self, task_id: str) -> Optional[TaskResponse]:
        """获取任务"""
        return self.tasks.get(task_id)
    
    def list_tasks(
        self, 
        project_id: Optional[str] = None,
        agent: Optional[AgentRole] = None,
        status: Optional[TaskStatus] = None
    ) -> List[TaskResponse]:
        """列出任务"""
        with self._lock:
            tasks = list(self.tasks.values())
            if project_id:
                tasks = [t for t in tasks if t.project_id == project_id]
            if agent:
                tasks = [t for t in tasks if t.assigned_agent == agent]
            if status:
                tasks = [t for t in tasks if t.status == status]
            return sorted(tasks, key=lambda x: (x.priority, x.created_at), reverse=True)
    
    def update_task(self, task_id: str, **kwargs) -> Optional[TaskResponse]:
        """更新任务"""
        with self._lock:
            task = self.tasks.get(task_id)
            if not task:
                return None
            for key, value in kwargs.items():
                if value is not None and hasattr(task, key):
                    setattr(task, key, value)
            task.updated_at = datetime.utcnow()
            
            # 更新项目任务列表引用
            project = self.projects.get(task.project_id)
            if project:
                for i, t in enumerate(project.tasks):
                    if t.id == task_id:
                        project.tasks[i] = task
                        break
            
            # 状态变更时更新时间戳
            if kwargs.get("status") == TaskStatus.RUNNING and not task.started_at:
                task.started_at = datetime.utcnow()
            if kwargs.get("status") in (TaskStatus.COMPLETED, TaskStatus.FAILED):
                task.completed_at = datetime.utcnow()
                # 从待办队列移除
                if task.assigned_agent in self.pending_tasks:
                    if task_id in self.pending_tasks[task.assigned_agent]:
                        self.pending_tasks[task.assigned_agent].remove(task_id)
            
            return task
    
    def delete_task(self, task_id: str) -> bool:
        """删除任务"""
        with self._lock:
            task = self.tasks.get(task_id)
            if not task:
                return False
            project = self.projects.get(task.project_id)
            if project:
                project.tasks = [t for t in project.tasks if t.id != task_id]
            del self.tasks[task_id]
            return True
    
    # ============== 任务派发 ==============
    
    def dispatch_task(self, project_id: str, task_id: str, message: str = "") -> bool:
        """派发任务给对应 Agent"""
        with self._lock:
            task = self.tasks.get(task_id)
            if not task or task.project_id != project_id:
                return False
            
            task.status = TaskStatus.PENDING
            task.description = f"{task.description}\n\n[CEO Dispatch]: {message}".strip()
            task.updated_at = datetime.utcnow()
            
            # 更新团队成员当前任务
            team = self.teams.get(project_id)
            if team:
                for member in team.members:
                    if member.role == task.assigned_agent:
                        member.current_task_id = task_id
                        break
            
            logger.info(f"Dispatched task {task_id} to {task.assigned_agent}")
            return True
    
    # ============== 团队操作 ==============
    
    def get_team(self, project_id: str) -> Optional[ProjectTeam]:
        """获取项目团队"""
        return self.teams.get(project_id)
    
    # ============== Graph State 操作 ==============
    
    def get_graph_state(self, project_id: str) -> Optional[GraphState]:
        """获取 LangGraph 状态"""
        return self.graph_states.get(project_id)
    
    def update_graph_state(self, project_id: str, **kwargs) -> Optional[GraphState]:
        """更新 LangGraph 状态"""
        with self._lock:
            state = self.graph_states.get(project_id)
            if not state:
                return None
            for key, value in kwargs.items():
                if hasattr(state, key):
                    setattr(state, key, value)
            return state


# 全局单例
store = InMemoryStore()
