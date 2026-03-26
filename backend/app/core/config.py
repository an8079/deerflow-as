"""
DeerFlow-X 后端配置
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "DeerFlow-X"
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/api/v1"
    
    # Supabase 配置（可选，用于持久化存储）
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None
    SUPABASE_SERVICE_KEY: Optional[str] = None
    
    # Redis 配置（可选，用于分布式任务队列）
    REDIS_URL: Optional[str] = None
    
    # LLM 配置（硅基流动 SiliconFlow）
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", None)
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.siliconflow.cn/v1")

    # 模型分层策略（省钱 + 质量兼顾）
    # 简单任务：成本极低，速度快
    MODEL_LIGHT: str = "deepseek-ai/DeepSeek-V3.2"
    # 复杂Agent任务：性能优先
    MODEL_PRO: str = "deepseek-ai/DeepSeek-V3"
    # 深度推理：最高质量
    MODEL_MAX: str = "deepseek-ai/DeepSeek-R1"

    # 默认用轻量模型，省钱
    OPENAI_MODEL: str = "deepseek-ai/DeepSeek-V3.2"
    
    # Agent 配置
    MAX_CONCURRENT_PROJECTS: int = 10
    TASK_TIMEOUT_SECONDS: int = 300
    
    # 安全配置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "deerflow-x-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# 硅基流动 API Key（用户已提供）
_siliconflow_key = "sk-pvqbgxpyqojhhibldeycmhohogdipzxkoswtsgpcixrftutj"
if not settings.OPENAI_API_KEY:
    settings.OPENAI_API_KEY = _siliconflow_key
