FROM python:3.7

COPY . /app

WORKDIR /app

RUN pip install -U pip
RUN pip config set global.index-url http://mirrors.aliyun.com/pypi/simple
RUN pip config set install.trusted-host mirrors.aliyun.com

RUN pip install -r requirements.txt \
    && groupadd -r admin && useradd -r -g admin admin \
    && chown -R admin:admin /app \
    && chmod 777 /app

USER admin

ENTRYPOINT ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]
