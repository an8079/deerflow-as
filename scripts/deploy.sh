#!/bin/bash
set -e
echo "=== DeerFlow-X 部署脚本 ==="
echo "[1/4] 检查环境变量..."
[ -z "$SUPABASE_URL" ] && echo "❌ SUPABASE_URL 未设置" && exit 1
[ -z "$OPENAI_API_KEY" ] && echo "❌ OPENAI_API_KEY 未设置" && exit 1
echo "[2/4] 构建 Docker 镜像..."
docker build -t deer-flow-x:latest .
echo "[3/4] 启动服务..."
docker run -d --name deer-flow-api -p 8000:8000 -e SUPABASE_URL=$SUPABASE_URL -e OPENAI_API_KEY=$OPENAI_API_KEY deer-flow-x:latest
echo "[4/4] 前端构建..."
cd frontend && npm install && npm run build && cd ..
echo "✅ 部署完成! API: http://localhost:8000"
