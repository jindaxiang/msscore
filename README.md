## 介绍

这是 msscore 的官方项目地址，本项目主要解决在 Jupyter Notebook 或 JupyterLab 中对题目进行记录及评分对问题。

## 使用

### 开启后台接口

```shell
python score_server.py
```

### 在 Jupyter 中使用

```python
import msscore as mc

score = mc.score("answer")  # 其中的 answer 为答案文件，由 YAML 格式的文件构成

q_1 = [1, 2, 3]  # 用户做的答案
score.judge('q_1', q_1)  # 其中 `'q_1'` 为答案的索引（由管理员制定，必须一致），`q_1` 变量为答案，可以定义不同的变量名
score.result  # 用户可以查看当前的成绩
score.save()  # 用户可以提交成绩
```

## 项目架构

本项目分为评分库 mssocre 和其后台系统，评分库主要用来记录答题的数据，后台系统则将所有数据整合起来，提交给教师进行预览

## 主要技术栈

### FastAPI

主要用于搭建数据库提交数据的接口

### SQLModel

主要用于解决数据库与数据模型的映射

### MySQL

后台数据库选择 MySQL 来进行管理

## 异常处理

### MySQLDB 缺失

需要把如下代码放到报错的文件中如下：

```python
import pymysql

pymysql.install_as_MySQLdb()
```
