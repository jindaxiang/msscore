# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/8/25 18:37
Desc: 测试文件
"""
import msscore as mc

q_1 = [1, 2, 3, 4]
q_2 = {"animal": "pig", "fruit": "apple", }
score = mc.score("answer")
score.judge("q_1", q_2)
score.judge("q_1", q_2)
score.judge("q_2", q_2)
score.judge("q_2", q_2)
score.judge("q_2", q_2)
score.judge("q_2", q_2)
score.judge("q_2", q_2)
score.judge("q_2", q_1)
score.judge("q_2", {1, 3, 4})
score.judge("q_2", {1, 3, 4, 5})
score.result
score.save()
