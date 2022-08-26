# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/8/26 16:31
Desc: 
"""
from fastapi import FastAPI, APIRouter
import uvicorn
from my_model import engine, Score
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pydantic import BaseModel


class UserScore(BaseModel):
    user_name: str
    right_num: int
    wrong_num: int


app = FastAPI()


@app.post("/")
async def get_root(user_socre: UserScore):
    print(user_socre.dict())
    print(type(user_socre))
    score = Score(**user_socre.dict())
    with Session(engine) as session:
        session.add(score)
        session.commit()
    return {"msg": "success"}


@app.get("/result")
async def get_root(user_name: str = "king"):
    print(user_name)
    statement = select(Score).where(Score.user_name == user_name)
    with Session(engine) as session:
        results = session.exec(statement)
        return results.all()

if __name__ == '__main__':
    uvicorn.run("score_server:app", reload=True)
