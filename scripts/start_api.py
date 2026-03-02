"""
启动 FastAPI 服务
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import uvicorn
from src.utils.config import settings
from src.utils.logger import logger


def main():
    """启动 API 服务"""
    logger.info(f"启动 {settings.APP_NAME} API 服务...")
    logger.info(f"服务地址: http://{settings.API_HOST}:{settings.API_PORT}")
    logger.info(f"API 文档: http://{settings.API_HOST}:{settings.API_PORT}/docs")

    uvicorn.run(
        "src.api.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
        log_level="info"
    )


if __name__ == "__main__":
    main()
