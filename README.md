# 🦌 DeerFlow-X

> **Solo Prenuers OS** — 让一个人+AI团队替代3-10人初创工作室

在 [ByteDance DeerFlow 2.0](https://github.com/bytedance/deer-flow) 基础上二次开发，构建AI团队协作操作系统，2026年下半年商业化。

[![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/deer-flow-x)](https://github.com/YOUR_USERNAME/deer-flow-x)
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
- 🚀 **一键部署** — Vercel/Railway 自动构建上线
- 💰 **内置计费** — Stripe 订阅，用户管理

## 🚀 5分钟快速开始

```bash
# 1. 克隆
git clone https://github.com/YOUR_USERNAME/deer-flow-x.git
cd deer-flow-x

# 2. 配置环境变量
cp .env.example .env
# 填入你的 ANTHROPIC_API_KEY 等

# 3. 一键启动
docker-compose up -d

# 4. 打开浏览器
open http://localhost:5173
```

## 📁 项目结构

```
deer-flow-x/
├── backend/              # FastAPI + LangGraph 后端
│   ├── app/
│   │   ├── api/         # REST API 路由
│   │   ├── core/        # 配置、日志、工具
│   │   ├── models/      # Pydantic 数据模型
│   │   └── services/     # 业务逻辑
│   ├── tests/           # 测试
│   └── main.py          # 入口
├── frontend/            # React + TypeScript 前端
│   ├── src/
│   │   ├── components/  # UI 组件
│   │   ├── pages/       # 页面
│   │   └── hooks/       # React hooks
│   └── package.json
├── docs/                # 产品文档
│   ├── PRODUCT-ROADMAP.md
│   ├── MVP-SPEC.md
│   └── ARCHITECTURE.md
├── docker-compose.yml   # Docker 编排
├── Dockerfile           # 后端镜像
└── DEPLOY.md            # 部署指南
```

## 🤝 团队角色

| 角色 | Agent ID | 职责 |
|------|----------|------|
| 👔 CEO | deerflow-x-ceo | 监视团队、分解任务、PUA |
| 🏗️ 架构师 | architect | 系统设计、技术选型 |
| 👨‍💻 程序员A | dev-backend | 后端 FastAPI/LangGraph |
| 👩‍💻 程序员B | dev-frontend | 前端 React/Tailwind |
| 🧪 测试 | qa | 测试、找茬、保证质量 |
| 🚀 运维 | ops | Docker/CI/CD/部署 |

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| 核心引擎 | Python 3.11 + FastAPI + LangGraph |
| 前端 | React 18 + TypeScript + TailwindCSS |
| 数据库 | PostgreSQL 15 + Redis 7 |
| AI模型 | MiniMax M2.7 Highspeed |
| 部署 | Docker + Railway + Vercel |
| 支付 | Stripe |

## 📈 Roadmap

- [x] 架构设计
- [ ] MVP (2026-Q3)
- [ ] Pro/Team 订阅 (2026-Q3)
- [ ] 开源发布 (2026-Q4)
- [ ] $50K MRR (2027-Q1)

## 📖 文档

- [产品路线图](docs/PRODUCT-ROADMAP.md)
- [MVP功能规格](docs/MVP-SPEC.md)
- [架构设计](docs/ARCHITECTURE.md)
- [商业化策略](STRATEGY.md)
- [部署指南](DEPLOY.md)

## License

MIT © 2026 DeerFlow-X Team
