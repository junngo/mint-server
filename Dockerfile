FROM python:3.8-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y libpq-dev gcc

COPY . /usr/src/app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
