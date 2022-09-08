# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/9/8 15:20
Desc: 数据模型层
参考文章：
https://cloud.tencent.com/developer/article/1949682
"""
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime


class Score(BaseModel):
    # id: int
    user_name: str = "test"
    answer_title: str = "test"
    answer_detail: str = "test"
    answer_result: str = "test"
    # created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True


if __name__ == "__main__":
    external_data = {
        "id": 1,
        "user_name": "king",
        "answer_title": "python_list",
        "answer_detail": "answer_detail",
        "answer_result": "answer_result",
        "created_at": datetime.now(),
    }
    try:
        Score(**external_data)
    except ValidationError as e:
        print(e.json())
    score = Score(**external_data)
    print(score.json())
