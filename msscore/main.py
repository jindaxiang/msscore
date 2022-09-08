# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/8/26 16:31
Desc: FastAPI 服务，用于接收判分的结果
"""
import uvicorn
from fastapi import FastAPI, status, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

template = Jinja2Templates("../static")

from database import engine
from msscore import models
from msscore import schemas
from msscore.database import SessionLocal
import msscore.crud as crud

models.Base.metadata.create_all(engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/", response_model=schemas.Score, response_model_exclude={'answer_result'})
async def get_root(user_score: schemas.Score, db: Session = Depends(get_db)):
    """
    提交 Post 数据接口
    :param user_score:
    :type user_score:
    :param db:
    :type db:
    :return:
    :rtype:
    """
    return crud.create_user(db, user_score)


@app.get("/result")
async def get_root(user_name: str = "king", db: Session = Depends(get_db)):
    """
    查看用户的情况
    :param user_name: 用户名
    :type user_name: str
    :param db:
    :type db:
    :return: 保存数据
    :rtype: None
    """
    return crud.get_user(db, user_name)


@app.get("/show")
async def show(
        request: Request, user_name: str = "king", db: Session = Depends(get_db)
):
    first_all = crud.get_user(db, user_name)
    return template.TemplateResponse(
        "index.html",
        context={"request": request, "msg": first_all.user_name},
    )


@app.post("/todo", status_code=status.HTTP_201_CREATED)
def todo(username=Form(None), password=Form(None)):
    print({username: password})
    return RedirectResponse(f"/show?user_name={username}")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", debug=True)
