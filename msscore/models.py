# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/9/8 15:20
Desc: ORM 映射
"""
import sqlalchemy as sa

from msscore.database import Base


class Score(Base):
    """
    数据模型
    """

    __tablename__ = "score"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False, comment="主键ID")
    user_name = sa.Column(sa.String(100), comment="用户名")
    answer_title = sa.Column(sa.String(100), comment="答案文件名")
    answer_detail = sa.Column(sa.Text(100), comment="答案详情")
    answer_result = sa.Column(sa.Text(100), comment="答案结果")
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now(), comment="回答时间")

