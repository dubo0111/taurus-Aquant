"""
日志工具模块（简化版，使用标准库）
"""
import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger():
    """配置日志系统（简化版）"""

    # 创建根 logger
    logger = logging.getLogger("TaurusAQuant")
    logger.setLevel(logging.DEBUG)

    # 移除已有的 handlers
    logger.handlers.clear()

    # 控制台输出
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # 文件输出
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # 应用日志
    file_handler = logging.FileHandler(
        log_dir / f"app_{datetime.now().strftime('%Y-%m-%d')}.log",
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s'
    )
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    # 错误日志单独文件
    error_handler = logging.FileHandler(
        log_dir / f"error_{datetime.now().strftime('%Y-%m-%d')}.log",
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_format)
    logger.addHandler(error_handler)

    return logger


# 初始化 logger
logger = setup_logger()
