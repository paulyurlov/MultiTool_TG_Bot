# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster


RUN pip3 install -r requirements.txt

COPY . .

ENV TZ="Europe/Moscow"

CMD [ "python3", "bot.py"]