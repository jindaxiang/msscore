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
        self.answer_title = None
        self.answer_result = {}
        self.answer_detail = {}
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

    def get_answer(self, file_name: str = "answer"):
        self.answer_title = file_name
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
        self.answer_detail[f"{q_name}_total_num"] = self.answer_detail.get(f"{q_name}_total_num", 0) + 1
        print('---------------', self.answer)
        previous_name = str(q_name)
        present_name = str(q_name)
        if str(q_name) in self.answer:
            answer_result = self.answer[str(q_name)]
            if answer_result == q_value:
                self.right_answer = self.right_answer + 1
                print('flag', str(q_name), self.right_answer + 1)
                self.answer_detail[f"{str(q_name)}_total_right_num"] = self.right_answer
                return "回答正确"
            else:
                self.wrong_answer = self.wrong_answer + 1
                self.answer_detail[f"{str(q_name)}_total_wrong_num"] = self.wrong_answer
                return "回答错误"
        else:
            return "请输入正确的变量名称和变量"

    @property
    def result(self):
        return {"回答正确": self.right_answer, "回答错误": self.wrong_answer}

    def save(self):

        url = "http://127.0.0.1:8000"
        right_num = len([value for key, value in self.answer_detail.items() if key.endswith("total_right_num") and value!=0])
        all_num = len([value for key, value in self.answer_detail.items() if key.endswith("total_num")])
        self.answer_result['right_rate'] = right_num / all_num
        self.answer_result['right_question'] = ['_'.join(key.split("_")[:2]) for key, value in self.answer_detail.items() if key.endswith("total_right_num") and value!=0]
        self.answer_result['wrong_question'] = list({'_'.join(key.split("_")[:2]) for key, value in self.answer_detail.items() if key.endswith("total_num")} - set(self.answer_result['right_question']))
        payload = {
            "user_name": self.name,
            "right_num": self.right_answer,
            "wrong_num": self.wrong_answer,
            "answer_title": self.answer_title,
            "answer_detail": str(self.answer_detail),
            "answer_result": str(self.answer_result),
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
