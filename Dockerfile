FROM python:3.11.8-bullseye

COPY ./ /app
WORKDIR /app

RUN apt-get update -y && \
    apt-get install gettext -y && \
    pip install -r requirements/base.txt
