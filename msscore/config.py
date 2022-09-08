# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/9/8 15:20
Desc: 配置文件
"""
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """
    数据库配置模型类
    """
    env_name: str = "Local"
    mysql_db: str = "score"
    mysql_user: str = "root"
    mysql_passwd: str = "king"
    mysql_host: str = "127.0.0.1"
    mysql_port: int = 3306

    class Config:
        env_file = "../.env"


class LocalSettings(Settings):
    pass


class ServerSettings(Settings):
    env_name: str = "Server"
    base_url: str = "1.1.1.1:8000"
    db_url: str = "mysql+pymysql://root@king"

    class Config:
        env_file = "../.env"


@lru_cache
def get_local_settings() -> Settings:
    settings = LocalSettings()
    print(f"Loading local settings for: {settings.env_name}")
    return settings
