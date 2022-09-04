# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/8/26 16:31
Desc: FastAPI 服务，用于接收判分的结果
"""
import uvicorn
from fastapi import FastAPI, status, Request, Form
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from sqlalchemy import Column, TEXT
from sqlmodel import Session, select, Field
from fastapi.templating import Jinja2Templates

template = Jinja2Templates("../static")

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
    提交 Post 数据接口
    :param user_score:
    :type user_score:
    :return:
    :rtype:
    """
    score = Score(**user_score.dict())
    with Session(engine) as session:
        session.add(score)
        session.commit()
        return JSONResponse({"msg": "success"},
                            status_code=status.HTTP_201_CREATED
                            )


@app.get("/result")
async def get_root(user_name: str = "king"):
    """
    查看用户的情况
    :param user_name: 用户名
    :type user_name: str
    :return: 保存数据
    :rtype: None
    """
    statement = select(Score).where(Score.user_name == user_name)
    with Session(engine) as session:
        results = session.exec(statement)
        return results.all()


@app.get("/show")
async def show(request: Request, name: str = "king"):
    statement = select(Score).where(Score.user_name == name)
    with Session(engine) as session:
        results = session.exec(statement)
        first_all = results.first()
    return template.TemplateResponse("index.html", context={'request': request, 'msg': first_all.user_name},)


@app.post('/todo', status_code=status.HTTP_201_CREATED)
def todo(username=Form(None), password=Form(None)):
    print({username: password})
    return RedirectResponse(f'/show?user_name={username}')


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1")
