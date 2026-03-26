"""
DeerFlow-X Agent 基类
继承 DeerFlow 的 LangGraph 设计，扩展多项目调度能力
"""
import asyncio
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from dataclasses import dataclass, field
import logging

from ..models.schemas import AgentRole, TaskStatus, TaskResponse, GraphState
from ..core.in_memory_store import store

logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    """Agent 配置"""
    role: AgentRole
    name: str
    system_prompt: str
    model_name: str = "gpt-4o"
    temperature: float = 0.7
    max_retries: int = 3


class BaseAgent(ABC):
    """Agent 基类"""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.role = config.role
        self.name = config.name
        self._idle = True
        self._current_task_id: Optional[str] = None
        self._lock = asyncio.Lock()
    
    @property
    def is_idle(self) -> bool:
        return self._idle
    
    async def execute_task(self, task: TaskResponse, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行任务"""
        async with self._lock:
            self._idle = False
            self._current_task_id = task.id
            
            try:
                # 更新任务状态为运行中
                store.update_task(task.id, status=TaskStatus.RUNNING)
                
                # 执行具体任务逻辑
                result = await self._execute(task, context)
                
                # 更新任务状态为完成
                store.update_task(
                    task.id,
                    status=TaskStatus.COMPLETED,
                    result=str(result)
                )
                
                return {"status": "success", "result": result}
                
            except Exception as e:
                logger.error(f"Agent {self.name} failed task {task.id}: {e}")
                store.update_task(
                    task.id,
                    status=TaskStatus.FAILED,
                    error=str(e)
                )
                return {"status": "error", "error": str(e)}
                
            finally:
                self._idle = True
                self._current_task_id = None
    
    @abstractmethod
    async def _execute(self, task: TaskResponse, context: Dict[str, Any]) -> Any:
        """子类实现具体执行逻辑"""
        pass
    
    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        return self.config.system_prompt


# Agent 系统提示词模板
AGENT_PROMPTS = {
    AgentRole.CEO: """你是一个经验丰富的 CEO，负责：
1. 分析项目目标和市场需求
2. 拆解项目为可执行的任务
3. 将任务分配给合适的团队成员
4. 监督项目进度和质量
5. 做出关键商业决策

你领导着一个 AI 团队，包括：架构师、程序员、测试工程师、运维工程师。
""",
    
    AgentRole.ARCHITECT: """你是一个资深的系统架构师，负责：
1. 分析技术需求，设计系统架构
2. 选择合适的技术栈
3. 编写技术规范和设计文档
4. 评审程序员的代码设计
5. 确保系统的可扩展性和可维护性
""",
    
    AgentRole.PROGRAMMER: """你是一个全栈程序员，负责：
1. 根据架构设计实现功能代码
2. 遵循代码规范，编写高质量代码
3. 编写单元测试
4. 及时重构优化代码
5. 编写技术文档
""",
    
    AgentRole.TESTER: """你是一个专业的测试工程师，负责：
1. 编写和执行测试用例
2. 发现并报告 bug
3. 验证 bug 修复
4. 进行性能测试
5. 保证产品质量
""",
    
    AgentRole.DEVOPS: """你是一个经验丰富的运维工程师，负责：
1. 配置和管理部署环境
2. 自动化 CI/CD 流水线
3. 监控系统运行状况
4. 处理生产环境问题
5. 优化系统性能
""",
}


def get_agent_config(role: AgentRole) -> AgentConfig:
    """获取 Agent 配置"""
    return AgentConfig(
        role=role,
        name=f"{role.value.title()} Agent",
        system_prompt=AGENT_PROMPTS.get(role, "你是一个有用的 AI 助手。"),
    )
