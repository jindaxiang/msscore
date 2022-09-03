# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/8/26 16:49
Desc: 模型层
"""
from typing import Optional

from sqlmodel import Field, SQLModel, create_engine
from sqlalchemy import Column, TEXT
from datetime import datetime


class Score(SQLModel, table=True):
    """
    数据模型
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str
    answer_title: str
    answer_detail: str = Field(sa_column=Column(TEXT))
    answer_result: str
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)


MYSQL_DB = "score"  # MySQL 数据库名称
MYSQL_USER = "root"  # MySQL 数据库登录帐号
MYSQL_PASSWD = "-"  # MySQL 数据库登陆密码，由于格式化路径的问题，请勿使用 `@` 符号
# MYSQL_PASSWD = "-"  # MySQL 数据库登陆密码，由于格式化路径的问题，请勿使用 `@` 符号
# MYSQL_HOST = "127.0.0.1"  # MySQL 数据库地址，此处需要替换为服务器的地址
MYSQL_HOST = "-"  # MySQL 数据库地址，此处需要替换为服务器的地址
MYSQL_POST = 3306  # MySQL 端口
# 注意其中必须设置中文字符串，否则会对存储中文有报错
mysql_url = f"mysql://{MYSQL_USER}:{MYSQL_PASSWD}@{MYSQL_HOST}:{MYSQL_POST}/{MYSQL_DB}?charset=utf8"
engine = create_engine(mysql_url, echo=True)
SQLModel.metadata.create_all(engine)
