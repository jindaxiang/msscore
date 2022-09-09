# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/8/26 16:31
Desc: FastAPI 服务，用于接收判分的结果
"""
import uvicorn
from fastapi import FastAPI, status, Request, Form, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from msscore.auth import (
    oauth2_scheme,
)

template = Jinja2Templates("../static")

from database import engine
from msscore import models
from msscore import schemas
from msscore.database import SessionLocal
import msscore.crud as crud
from msscore.schemas import Token
from fastapi.security import OAuth2PasswordRequestForm
from msscore.crud import authenticate_user, create_access_token, get_current_active_user
from msscore.auth import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta


models.Base.metadata.create_all(engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/token", response_model=Token)
async def login_for_access_token(
    db=Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    current_user = await get_current_active_user(db=db, token=token)
    type(current_user)
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    current_user = await get_current_active_user(db=db, token=token)
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.post("/", response_model=schemas.Score, response_model_exclude={"answer_result"})
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
    return crud.create_socre(db, user_score)


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
    return crud.get_score(db, user_name)


@app.get("/show")
async def show(
    request: Request, user_name: str = "king", db: Session = Depends(get_db)
):
    first_all = crud.get_score(db, user_name)
    return template.TemplateResponse(
        "index.html",
        context={"request": request, "msg": first_all[0].user_name},
    )


@app.post("/todo", status_code=status.HTTP_201_CREATED)
def todo(username=Form(None), password=Form(None)):
    print({username: password})
    return RedirectResponse(f"/show?user_name={username}")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", debug=True)
