FROM python:3.8.1-alpine

WORKDIR /code/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /code/src/requirements.txt

RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
        libressl-dev libffi-dev gcc musl-dev python3-dev \
    && pip install --upgrade pip setuptools wheel \
    && pip install fastapi uvicorn \
    && pip install -r /code/src/requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /code/src