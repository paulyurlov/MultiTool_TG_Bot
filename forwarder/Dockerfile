# syntax=docker/dockerfile:1

FROM ubuntu
FROM python:3.10-slim-buster

COPY . .

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get -y install gcc mono-mcs && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN apt install gcc
RUN pip3 install uWSGI

ENV TZ="Europe/Moscow"

CMD ["uwsgi", "--http", "0.0.0.0:69", "--wsgi-file", "app.py", "--callable", "app", "--stats", "0.0.0.0:81"]