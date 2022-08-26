# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/8/25 18:33
Desc: 
"""
import sys
import yaml
from typing import Any
import os
import requests


class Score:
    def __init__(self, file_name):
        self.name = self.get_user_name()
        self.file_name = file_name
        self.answer = self.get_answer(file_name)
        self.right_answer = 0
        self.wrong_answer = 0

    @classmethod
    def get_user_name(cls):
        # 获取 Ubuntu 系统的用户名
        user_name = sys.path[0].split("/")[-1].split("-")[-1]
        user_name = "albert"  # 测试代码
        return user_name

    @staticmethod
    def get_answer(file_name: str = "answer"):
        file_address = os.path.abspath(__file__).rsplit("\\", maxsplit=1)[0] + '\\' + file_name
        f = open(
            rf"{file_address}.yaml",
            "r",
        )
        data = yaml.load(f, Loader=yaml.FullLoader)
        question_list = list(data.keys())
        answer_dict = {}
        for i in range(0, len(data.keys())):
            answer_dict.update(
                {question_list[i]: eval(data[question_list[i]])}
            )
        return answer_dict

    def judge(self, q_name: str = None, q_value: Any = "hello"):
        if str(q_name) in self.answer:
            answer_result = self.answer[str(q_name)]
            if answer_result == q_value:
                self.right_answer = self.right_answer + 1
                return "回答正确"
            else:
                self.wrong_answer = self.wrong_answer + 1
                return "回答错误"
        else:
            return "请输入正确的变量名称和变量"

    @property
    def result(self):
        return {"回答正确": self.right_answer, "回答错误": self.wrong_answer}

    def save(self):
        url = "http://127.0.0.1:8000"
        payload = {
            "user_name": self.name,
            "right_num": self.right_answer,
            "wrong_num": self.wrong_answer
        }
        r = requests.post(url, json=payload)
        if r.status_code == 200:
            return {"msg": "success"}
        else:
            return {"msg": "fail"}


if __name__ == "__main__":
    q_1 = [1, 2, 3, 4]
    q_2 = {"fruit": "apple", "animal": "pig"}
    score = Score("answer")
    score.judge("q_1", q_1)
    score.result
