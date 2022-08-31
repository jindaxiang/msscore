# https://hub.docker.com/layers/python/library/python/3.10.1-buster/images/sha256-d59f2d9d7f17d34ad8e0c4aff37e61b181018413078ab8f0a688319ebee65d30?context=explore
FROM python:3.10.6-buster

MAINTAINER MaxSwell <daxiang.jin@maxsdsp.com>

# time-zone
RUN set -x \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt install -y tzdata \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai  /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir fastapi[all] -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com  --upgrade
RUN pip install --no-cache-dir uvicorn[standard] -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com  --upgrade
RUN pip install --no-cache-dir pyyaml -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com  --upgrade
RUN pip install --no-cache-dir sqlmodel -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com  --upgrade
RUN pip install --no-cache-dir mysqlclient -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com  --upgrade

COPY ./msscore /usr/local/lib/python3.10/site-packages/msscore

CMD ["python", "/usr/local/lib/python3.10/site-packages/msscore/score_server.py"]
