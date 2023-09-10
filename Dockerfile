FROM python:3.8-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_ROOT_USER_ACTION=ignore

RUN apt-get update

COPY . /usr/src/app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
