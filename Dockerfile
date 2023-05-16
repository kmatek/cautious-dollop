FROM python:3.11.3-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt

COPY ./app /app

WORKDIR /app

RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt