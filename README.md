# 🦌 DeerFlow-X

> **Solo Preneurs OS** — 让一个人+AI团队替代3-10人初创工作室

在 [ByteDance DeerFlow 2.0](https://github.com/bytedance/deer-flow) 基础上二次开发，构建AI团队协作操作系统，2026年下半年商业化。

[![CI](https://github.com/an8079/deerflow-as/actions/workflows/backend-test.yml/badge.svg)](https://github.com/an8079/deerflow-as/actions)
[![Frontend Build](https://github.com/an8079/deerflow-as/actions/workflows/frontend-build.yml/badge.svg)](https://github.com/an8079/deerflow-as/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 这是什么？

DeerFlow-X = **DeerFlow 2.0** + **多项目团队管理** + **商业化模块**

- 一个人 + AI团队 = 独立开发者工作室
- 目标：2026年下半年让独立开发者用AI替代小团队
- 定价：Pro $19/月 · Team $49/月 · Enterprise $199/月

## ✨ 核心功能

- 🏢 **多项目管理** — 同时跑多个项目，独立记忆上下文
- 🤖 **AI团队** — CEO/架构师/程序员/测试/运维，各司其职
- 📊 **实时仪表盘** — 看着AI团队帮你干活
- 🚀 **一键部署** — Docker / Railway / Vercel 自动构建上线
- 💰 **内置计费** — Stripe 订阅，用户管理

---

## 📋 前置要求

| 软件 | 最低版本 | 说明 |
|------|---------|------|
| Docker | 20.x | 容器化运行后端+数据库 |
| Docker Compose | 2.x | 多容器编排 |
| Python | 3.11 | 本地后端开发 |
| Node.js | 18.x | 前端开发 |

---

## 🚀 快速开始

### Docker 一键启动（推荐）

```bash
git clone https://github.com/an8079/deerflow-as.git
cd deerflow-as
cp .env.example .env
# 编辑 .env 填入你的 OPENAI_API_KEY 等
docker-compose up -d
open http://localhost:5173
```

### 本地开发（前后端分离）

```bash
git clone https://github.com/an8079/deerflow-as.git
cd deerflow-as
cp .env.example .env

# 后端
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# 前端（新终端）
cd frontend && npm install && npm run dev
# 访问 http://localhost:5173
```

---

## 🔧 环境变量

```env
DATABASE_URL=postgresql+asyncpg://deerflow:changeme@localhost:5432/deerflow
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=sk-your-key-here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SECRET_KEY=change-me-in-production
CORS_ORIGINS=http://localhost:5173
BACKEND_PORT=8000
```

---

## 🧪 本地测试

```bash
# 后端
cd backend && pip install -r ../requirements-test.txt && pytest tests/ -v

# 前端
cd frontend && npm run test -- --run
```

---

## 🐳 Docker 部署

```bash
docker-compose up -d --build          # 生产构建
docker-compose logs -f backend        # 查看日志
docker-compose --profile with-frontend up -d  # 带前端
docker-compose down                    # 停止
```

---

## ☁️ 云端部署

### Railway（推荐）

1. 连接 GitHub 到 railway.app
2. Railway 自动检测 Dockerfile 和 docker-compose.yml
3. 设置环境变量（OPENAI_API_KEY 等）
4. 部署完成，自动分配域名

### Vercel（前端）

```bash
cd frontend && npx vercel --prod
```

---

## 📁 项目结构

```
deer-flow-x/
├── backend/
│   ├── app/             # API routes, core, services
│   ├── tests/           # pytest 测试
│   ├── pytest.ini       # pytest 配置
│   └── main.py
├── frontend/
│   ├── src/             # 组件、页面、hooks
│   └── tests/           # Vitest 单元测试
├── .github/workflows/
│   ├── backend-test.yml  # Backend pytest
│   ├── frontend-build.yml # Frontend 构建
│   └── ci.yml           # Lint 检查
├── docs/
├── k8s/
├── docker-compose.yml
├── Dockerfile
├── Dockerfile.frontend
└── .env.example
```

---

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| 核心引擎 | Python 3.11 + FastAPI + LangGraph |
| 前端 | React 18 + TypeScript + TailwindCSS |
| 数据库 | PostgreSQL 15 + Redis 7 |
| 部署 | Docker + Railway + Vercel |
| 支付 | Stripe |

---

## 📖 文档

- [产品路线图](docs/PRODUCT-ROADMAP.md)
- [MVP功能规格](docs/MVP-SPEC.md)
- [架构设计](docs/ARCHITECTURE.md)
- [商业化策略](STRATEGY.md)
- [部署指南](DEPLOY.md)

## License

MIT © 2026 DeerFlow-X Team
