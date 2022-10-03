# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/9/8 15:20
Desc: 日志模块
"""
import os

from loguru import logger

from core import settings
from utils.create_dir import create_dir


# 创建日志文件名
def logger_file() -> str:
    """ 创建日志文件名 """
    log_path = create_dir(settings.LOGGER_DIR)
    print("log_path", settings.LOGGER_DIR)

    """ 保留日志文件夹下最大个数(本地调试用) 
    本地调式需要多次重启, 日志轮转片不会生效 """
    file_list = os.listdir(log_path)
    if len(file_list) > 3:
        os.remove(os.path.join(log_path, file_list[0]))

    # 日志输出路径
    return os.path.join(log_path, settings.LOGGER_NAME)


# 详见: https://loguru.readthedocs.io/en/stable/overview.html#features
logger.add(
    logger_file(),
    encoding=settings.GLOBAL_ENCODING,
    level=settings.LOGGER_LEVEL,
    rotation=settings.LOGGER_ROTATION,
    retention=settings.LOGGER_RETENTION,
    enqueue=True
)
