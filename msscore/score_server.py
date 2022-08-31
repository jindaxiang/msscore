# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/8/26 16:31
Desc: FastAPI 服务，用于接收判分的结果
"""
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import Column, TEXT
from sqlmodel import Session, select, Field

from my_model import engine, Score


class UserScore(BaseModel):
    """
    Post 数据验证
    """
    user_name: str
    answer_title: str
    answer_detail: str = Field(sa_column=Column(TEXT))
    answer_result: str


app = FastAPI()


@app.post("/")
async def get_root(user_score: UserScore):
    """
    根目录，仅做测试
    :param user_score:
    :type user_score:
    :return:
    :rtype:
    """
    print(user_score.dict())
    print(type(user_score))
    score = Score(**user_score.dict())
    with Session(engine) as session:
        session.add(score)
        session.commit()
    return {"msg": "success"}


@app.get("/result")
async def get_root(user_name: str = "king"):
    """
    提交 Post 数据接口
    :param user_name: 用户名
    :type user_name: str
    :return:
    :rtype:
    """
    print(user_name)
    statement = select(Score).where(Score.user_name == user_name)
    with Session(engine) as session:
        results = session.exec(statement)
        return results.all()


if __name__ == "__main__":
    uvicorn.run("score_server:app", reload=True)
