# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

COPY . .

RUN pip3 install -r requirements.txt

ENV TZ="Europe/Moscow"

CMD [ "flask", "run"]