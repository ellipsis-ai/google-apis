FROM python:3.6.1-alpine

RUN apk update && apk add build-base

RUN mkdir /usr/src/app
WORKDIR /usr/src/app
RUN  pip install --upgrade google-api-python-client

ENV PYTHONUNBUFFERED 1

COPY . .
