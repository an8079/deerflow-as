# DeerFlow-X 部署指南

> 运维工程师老黄出品 | 适用平台：Railway / Vercel / Koyeb
> 版本：v0.1.0 | 架构：FastAPI + PostgreSQL 15 + Redis 7 + React

## 部署前检查清单

- [ ] 代码已推送到 GitHub（GitHub Actions 依赖此前提）
- [ ] .env.example 复制为 .env 并填写真实密钥
- [ ] Docker Hub / GHCR / AWS ECR 账号已创建
- [ ] 各平台账号已注册

---

## 方式一：Railway（推荐，最简单）

Railway 可以一键部署带数据库的完整应用。

### 1. 安装 Railway CLI

```bash
npm install -g @railway/cli
railway login
```

### 2. 连接项目并添加服务

```bash
cd deer-flow-x
railway init
railway add --service db postgres
railway add --service redis redis
railway add --service backend
```

### 3. 配置环境变量

在 Railway Dashboard → Backend → Variables 中添加：

```
OPENAI_API_KEY=sk-xxx
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=xxx
SECRET_KEY=your-secret-key
DATABASE_URL=<从 Railway 自动注入>
REDIS_URL=redis://redis:<port>/0
```

### 4. 部署

```bash
railway up
```

部署后查看 URL：`railway status`

---

## 方式二：Vercel（前端子项目）

Vercel 适合纯前端部署，后端 API 需单独部署（Railway 或 Koyeb）。

### 1. 安装 Vercel CLI

```bash
npm i -g vercel
vercel login
```

### 2. 配置前端

```bash
cd frontend
vercel
```

按提示填写项目名称和配置。

### 3. 配置 API 地址

在 Vercel Dashboard 创建环境变量：

```
VITE_API_BASE_URL=https://your-railway-app.railway.app
```

### 4. GitHub Actions 自动部署

在 Vercel Dashboard → Settings → Tokens 创建 token，配置 GitHub Secrets：

```
VERCEL_TOKEN=xxxxx
VERCEL_ORG_ID=team_xxxxx
VERCEL_PROJECT_ID=prj_xxxxx
```

---

## 方式三：Koyeb（Docker 爱好者首选）

Koyeb 原生支持 Docker 镜像，全球边缘部署，无需配置负载均衡。

### 1. 安装 Koyeb CLI

```bash
brew install koyeb/cli
# 或
curl -sfL https://get.koyeb.com | sh
```

### 2. 推送 Docker 镜像

```bash
docker login registry.koyeb.io
docker build -t registry.koyeb.io/your-username/deerflow-x-api:latest -f Dockerfile .
docker push registry.koyeb.io/your-username/deerflow-x-api:latest
```

### 3. CLI 部署

```bash
koyeb app create deerflow-x-api \
  --docker registry.koyeb.io/your-username/deerflow-x-api:latest \
  --port 8000 \
  --env DATABASE_URL=$DATABASE_URL \
  --env REDIS_URL=$REDIS_URL \
  --env OPENAI_API_KEY=$OPENAI_API_KEY \
  --instance-type nano
```

### 4. Web Dashboard 部署

1. 登录 app.koyeb.com
2. 点击 Create App
3. 选择 Docker
4. 输入镜像地址
5. 配置环境变量
6. 选择实例类型（nano 免费，small 适合生产）
7. 点击 Deploy

---

## Docker Compose 本地启动（开发用）

```bash
cp .env.example .env
# 编辑 .env 填入真实值
docker compose up -d
docker compose logs -f backend
docker compose down -v
```

服务地址：

| 服务 | 地址 |
|------|------|
| 后端 API | http://localhost:8000 |
| API 文档 | http://localhost:8000/docs |
| 前端 | http://localhost:3000 |
| PostgreSQL | localhost:5432 |
| Redis | localhost:6379 |

---

## 生产环境推荐架构

```
                ┌─────────────┐
                │   Vercel    │
                │  (Frontend) │
                └──────┬──────┘
                       │ HTTPS
                       ▼
             ┌─────────────────────┐
             │   Railway / Koyeb   │
             │  FastAPI Backend    │
             │  (auto-scaled)       │
             └──────────┬───────────┘
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
      ┌──────────────┐   ┌──────────────┐
      │  Railway DB   │   │  Railway      │
      │ PostgreSQL 15  │   │  Redis 7      │
      └──────────────┘   └──────────────┘
```

---

## 常见问题

**Q: Railway 部署后连不上数据库？**
A: Railway 的 DATABASE_URL 是自动注入的，不要手动设置，直接引用 `$DATABASE_URL`。

**Q: Koyeb 启动报错 502？**
A: 健康检查失败。检查 Dockerfile 里是否暴露了 8000 端口，以及 `--host 0.0.0.0`。

**Q: Vercel 前端跨域报错？**
A: FastAPI 的 CORS 中间件已配置，生产环境需在 CORS_ORIGINS 加上你的 Vercel 域名。

**Q: 镜像构建失败？**
A: 检查是否有多平台构建问题（`--platforms linux/amd64`）。本地构建可去掉 `--platforms` 参数。

---

## 安全注意事项

1. **SECRET_KEY** — 生产环境必须设置强随机字符串，不能为空
2. **OPENAI_API_KEY** — 只放在后端环境变量中，前端绝对不要暴露
3. **POSTGRES_PASSWORD** — 生产环境使用 32 位以上随机密码
4. **.env 文件** — 确认 `.gitignore` 包含 `.env`，不要提交到 Git

---

*有问题找老黄，服务器挂了我来修。*
