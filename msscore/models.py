# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/9/8 15:20
Desc: ORM 映射
"""
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = sa.Column(
        sa.Integer, primary_key=True, autoincrement=True, nullable=False, comment="主键ID"
    )
    username = sa.Column(sa.String(20), nullable=False, comment="用户名")
    hashed_password = sa.Column(sa.String(300), nullable=False, comment="密码")
    email = sa.Column(sa.String(100), nullable=False, comment="邮箱")
    full_name = sa.Column(sa.String(100), nullable=False, comment="全名")
    disabled = sa.Column(sa.Boolean, default=0)
    created_at = sa.Column(sa.DateTime(), nullable=False, server_default=sa.func.now(), comment="回答时间")


class Score(Base):
    """
    数据模型
    """

    __tablename__ = "score"

    id = sa.Column(
        sa.Integer, primary_key=True, autoincrement=True, nullable=False, comment="主键ID"
    )
    user_name = sa.Column(sa.String, nullable=False, comment="用户名")
    answer_title = sa.Column(sa.String, nullable=False, comment="答案文件名")
    answer_detail = sa.Column(sa.Text, nullable=False, comment="答案详情")
    answer_result = sa.Column(sa.Text, nullable=False, comment="答案结果")
    created_at = sa.Column(sa.DateTime(), nullable=False, server_default=sa.func.now(), comment="回答时间")
