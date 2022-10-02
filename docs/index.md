# 欢迎来到 MSScore 官方文档

完整的文档请访问：[MSScore 官方文档](https://msscore.readthedocs.io/).

## 介绍

这是 msscore 的官方项目地址，本项目主要解决在 Jupyter Notebook 或 JupyterLab 中对题目进行记录及评分对问题。目前该项目已经迁移到 mssdk 中，
但是作为服务端的程序还在这个项目中，目前本项目的部署主要依赖 Docker 来完成。

## 开发工作

1. 登陆模块开发
2. 完善注释

## Redis 启动

```console
brew services start redis
```

## 使用

### 开启后台接口

```console
python main.py
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

```console
pip install mysqlclient
```

### 启动

```console
cd /usr/local/lib/python3.10/site-packages/msscore
python main.py  # 注意不能在 reload 设置 True
```