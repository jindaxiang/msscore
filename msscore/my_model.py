# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/8/26 16:49
Desc: 
"""
from typing import Optional

from sqlmodel import Field, SQLModel, create_engine
from sqlalchemy import Column, TEXT
from datetime import datetime


class Score(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str
    right_num: int
    wrong_num: int
    answer_title: str
    answer_detail: str = Field(sa_column=Column(TEXT))
    answer_result: str
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)


MYSQL_DB = 'score'  # 数据库命
MYSQL_USER = 'root'  # 数据库账号
MYSQL_PASSWD = 'king'  # 数据库登陆密码
MYSQL_HOST = '127.0.0.1'  # 数据库地址
MYSQL_POST = 3306  # 端口

mysql_url = f"mysql://{MYSQL_USER}:{MYSQL_PASSWD}@{MYSQL_HOST}:{MYSQL_POST}/{MYSQL_DB}"

engine = create_engine(mysql_url, echo=True)

SQLModel.metadata.create_all(engine)
