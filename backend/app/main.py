"""
DeerFlow-X 后端主入口
"""
import logging
import uuid
import time
from contextlib import asynccontextmanager
from typing import Callable

from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from .core.config import settings
from .api.projects import projects_router, tasks_router, ws_router
from .agents.workflow import scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# ─── 请求 ID 中间件 ────────────────────────────────────────────────────────────

class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    为每个请求注入 X-Request-ID 头，便于追踪和日志关联。
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
        request.state.request_id = request_id

        start_time = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception as exc:
            elapsed = time.perf_counter() - start_time
            logger.exception(
                "[%s] Unhandled exception after %.2fms: %s",
                request_id, elapsed * 1000, exc,
            )
            raise

        elapsed = time.perf_counter() - start_time
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time-Ms"] = f"{elapsed * 1000:.2f}"
        logger.info(
            "[%s] %s %s -> %d (%.2fms)",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            elapsed * 1000,
        )
        return response


# ─── 全局异常处理器 ───────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("DeerFlow-X Backend starting...")
    yield
    logger.info("DeerFlow-X Backend shutting down...")
    for project_id in scheduler.get_running_projects():
        await scheduler.stop_project_workflow(project_id)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="AI 团队协作操作系统 - 多项目调度引擎",
        lifespan=lifespan,
    )

    # ── CORS（生产级别）─────────────────────────────────────────────────────
    _cors_origins = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        # ⚠️ 生产环境请在此添加真实域名，例如:
        # "https://your-frontend.com",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=_cors_origins,       # 禁止使用 "*" 配合 credentials=True
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-Response-Time-Ms"],
        max_age=600,
    )

    # ── 请求 ID 中间件（放在 CORS 之后）─────────────────────────────────────
    app.add_middleware(RequestIDMiddleware)

    # ── 全局异常捕获 ───────────────────────────────────────────────────────
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        request_id = getattr(request.state, "request_id", "unknown")
        logger.exception("[%s] Global exception: %s", request_id, exc)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": str(exc),
                "request_id": request_id,
            },
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail,
                "status_code": exc.status_code,
            },
        )

    # ── 注册路由 ───────────────────────────────────────────────────────────
    app.include_router(projects_router, prefix=settings.API_PREFIX)
    app.include_router(tasks_router, prefix=settings.API_PREFIX)
    app.include_router(ws_router)   # WebSocket 无 API_PREFIX，路径为 /ws/...

    # ── 健康检查 & 根路由 ──────────────────────────────────────────────────
    @app.get("/")
    async def root():
        return {
            "name": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "status": "running",
            "docs": "/docs",
        }

    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "running_projects": scheduler.get_running_projects(),
        }

    return app


# 供 uvicorn 直接加载
app = create_app()
