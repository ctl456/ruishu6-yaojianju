"""日志配置模块"""
import sys
from loguru import logger

def setup_logger(level="INFO"):
    """配置日志"""
    logger.remove()
    logger.add(sys.stderr, level=level)
    return logger

# 导出配置好的logger
log = setup_logger()