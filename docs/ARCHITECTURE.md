# DeerFlow-X 系统架构 v1.0

## 核心设计原则
- **模块化**: 每个Agent独立职责，松耦合
- **可扩展**: 支持水平扩展，动态增减Agent节点
- **容错性**: 单点故障不影响整体系统
- **可观测性**: 全链路日志、追踪、监控

## 技术栈
- Backend: Python 3.11+ / LangGraph / FastAPI
- Frontend: React 18 / TypeScript / TailwindCSS / Vite
- Database: Supabase (PostgreSQL + Auth + Realtime)
- Deployment: Docker / Railway / Vercel

## LangGraph 节点定义
```python
class AgentState(TypedDict):
    task: str
    context: dict
    current_agent: str
    results: dict
    errors: list
    iteration: int
```
Nodes: orchestrator → research → writer → coder → reviewer → END
