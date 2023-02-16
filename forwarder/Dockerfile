# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

COPY . .

RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install uWSGI

ENV TZ="Europe/Moscow"

CMD ["uwsgi", "--http", "0.0.0.0:69", "--wsgi-file", "app.py", "--callable", "app", "--stats", "0.0.0.0:81"]