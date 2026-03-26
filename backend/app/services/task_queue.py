import asyncio
import logging
from typing import Dict, Optional
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from ..models.schemas import AgentRole, TaskResponse, TaskStatus
from ..core.in_memory_store import store

logger = logging.getLogger(__name__)

class QueuePriority(str, Enum):
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"

@dataclass
class QueuedTask:
    task_id: str
    project_id: str
    agent: AgentRole
    priority: QueuePriority
    enqueued_at: datetime = field(default_factory=datetime.utcnow)
    retries: int = 0

class TaskQueue:
    """Agent 任务队列管理器"""
    
    def __init__(self):
        self._priority_queues: Dict[AgentRole, Dict[QueuePriority, deque]] = {
            role: {p: deque() for p in QueuePriority} for role in AgentRole
        }
        self._processing: Dict[str, asyncio.Task] = {}
    
    def enqueue(self, task: TaskResponse, priority: QueuePriority = QueuePriority.NORMAL) -> None:
        queued = QueuedTask(task_id=task.id, project_id=task.project_id,
                          agent=task.assigned_agent, priority=priority)
        self._priority_queues[task.assigned_agent][priority].append(queued)
        logger.info(f"Enqueued task {task.id} for {task.assigned_agent} ({priority.value})")
    
    def dequeue(self, agent: AgentRole) -> Optional[QueuedTask]:
        for priority in [QueuePriority.HIGH, QueuePriority.NORMAL, QueuePriority.LOW]:
            queue = self._priority_queues[agent][priority]
            if queue:
                return queue.popleft()
        return None
    
    def peek(self, agent: AgentRole) -> Optional[QueuedTask]:
        for priority in [QueuePriority.HIGH, QueuePriority.NORMAL, QueuePriority.LOW]:
            queue = self._priority_queues[agent][priority]
            if queue:
                return queue[0]
        return None
    
    def get_queue_size(self, agent: Optional[AgentRole] = None) -> Dict[str, int]:
        if agent:
            return {p.value: len(self._priority_queues[agent][p]) for p in QueuePriority}
        return {f"{a.value}_{p.value}": len(self._priority_queues[a][p])
                for a in AgentRole for p in QueuePriority}

task_queue = TaskQueue()
