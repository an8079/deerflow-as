# DeerFlow-X Backend

AI 团队协作操作系统核心后端服务

## 技术栈
- Python 3.11+ / FastAPI / LangGraph / Pydantic

## 项目结构
```
backend/
├── app/
│   ├── main.py              # FastAPI 应用入口
│   ├── core/
│   │   ├── config.py       # 配置管理
│   │   └── in_memory_store.py  # 内存数据存储
│   ├── models/
│   │   └── schemas.py      # 数据模型（项目/任务/Agent角色）
│   ├── api/
│   │   └── projects.py     # 项目管理 API
│   ├── agents/
│   │   ├── base.py         # Agent 基类
│   │   └── workflow.py      # LangGraph 多项目调度引擎
│   └── services/
│       └── task_queue.py   # 任务队列服务
├── requirements.txt
└── README.md
```

## 快速开始

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

访问 http://localhost:8000/docs 查看 API 文档。

## 核心功能

### 1. 多项目并发管理
每个项目有独立的 LangGraph 工作流，互不干扰。

### 2. Agent 角色系统
| 角色 | 职责 |
|------|------|
| CEO | 目标拆解、任务分配 |
| Architect | 架构设计 |
| Programmer | 代码实现 |
| Tester | 测试 |
| DevOps | 部署运维 |

### 3. API 示例

```bash
# 创建项目
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "My SaaS", "goal": "Ship fast"}'

# 创建任务并派发
curl -X POST http://localhost:8000/api/v1/projects/{id}/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Build API", "assigned_agent": "architect", "priority": 10}'

# 启动工作流
curl -X POST http://localhost:8000/api/v1/projects/{id}/start
```

## 开发
```bash
# 启动服务
uvicorn app.main:app --reload --port 8000

# 单元测试
pytest tests/ -v
```
