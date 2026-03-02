"""
配置管理模块（简化版，无外部依赖）
"""
import os
from typing import Optional
from pathlib import Path


class Settings:
    """应用配置（简化版）"""

    def __init__(self):
        """从环境变量加载配置"""
        # 先加载 .env 文件
        self._load_env_file()

        # 应用基础配置
        self.APP_NAME = os.getenv("APP_NAME", "Taurus-AQuant")
        self.APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
        self.DEBUG = os.getenv("DEBUG", "true").lower() == "true"
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

        # Tushare 配置
        self.TUSHARE_TOKEN = os.getenv("TUSHARE_TOKEN", "")
        self.TUSHARE_API_URL = os.getenv("TUSHARE_API_URL", "http://tushare.xyz")

        # LLM 提供商配置
        self.LLM_PROVIDER = os.getenv("LLM_PROVIDER", "zhipu")

        # OpenAI 配置
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        self.OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
        self.OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

        # 智谱 AI 配置
        self.ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "")
        self.ZHIPU_MODEL = os.getenv("ZHIPU_MODEL", "glm-4")

        # PostgreSQL 配置
        self.POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
        self.POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
        self.POSTGRES_DB = os.getenv("POSTGRES_DB", "taurus_aquant")
        self.POSTGRES_USER = os.getenv("POSTGRES_USER", "taurus")
        self.POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "taurus123")

        # Redis 配置
        self.REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
        self.REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
        self.REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
        self.REDIS_DB = int(os.getenv("REDIS_DB", "0"))

        # API 服务配置
        self.API_HOST = os.getenv("API_HOST", "0.0.0.0")
        self.API_PORT = int(os.getenv("API_PORT", "8000"))
        self.API_RELOAD = os.getenv("API_RELOAD", "true").lower() == "true"

        # Streamlit 配置
        self.STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))
        self.STREAMLIT_SERVER_ADDRESS = os.getenv("STREAMLIT_SERVER_ADDRESS", "0.0.0.0")

        # 数据配置
        self.DATA_CACHE_DIR = os.getenv("DATA_CACHE_DIR", "./data/cache")
        self.DATA_UPDATE_TIME = os.getenv("DATA_UPDATE_TIME", "18:00")

        # 风控配置
        self.RISK_MAX_POSITION_PCT = float(os.getenv("RISK_MAX_POSITION_PCT", "0.3"))
        self.RISK_MAX_DAILY_TRADES = int(os.getenv("RISK_MAX_DAILY_TRADES", "10"))
        self.RISK_STOP_LOSS_PCT = float(os.getenv("RISK_STOP_LOSS_PCT", "-0.05"))
        self.RISK_STOP_PROFIT_PCT = float(os.getenv("RISK_STOP_PROFIT_PCT", "0.10"))

    def _load_env_file(self):
        """从 .env 文件加载环境变量"""
        # 尝试多个可能的路径
        possible_paths = [
            Path(".env"),
            Path.cwd() / ".env",
            Path(__file__).parent.parent.parent.parent / ".env"
        ]

        env_file = None
        for path in possible_paths:
            if path.exists():
                env_file = path
                break

        if env_file and env_file.exists():
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        # 直接设置到 os.environ（不检查是否已存在）
                        os.environ[key] = value

    @property
    def database_url(self) -> str:
        """获取数据库连接 URL"""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def redis_url(self) -> str:
        """获取 Redis 连接 URL"""
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


# 全局配置实例
settings = Settings()
