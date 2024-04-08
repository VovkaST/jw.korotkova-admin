FROM python:3.11.8-bullseye
LABEL authors="Korotkov Vladimir"

ENV TZ=Europe/Moscow
ENV DJANGO_SETTINGS_MODULE=root.settings
ENV PYTHONUNBUFFERED=1

COPY . /app

WORKDIR /app

RUN pip install -r requirements/base.txt

RUN python3 manage.py migrate bot

CMD python3 manage.py run_bot
