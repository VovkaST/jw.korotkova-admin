#!/bin/bash
YELLOW="\033[1;33m"
GREEN="\033[0;32m"
NORMAL="\033[0m"

echo -e "${YELLOW}Running admin-panel${NORMAL}"

source ./compose/migrations.sh
source ./compose/make_messages.sh

echo -e "${GREEN}Collecting static files...${NORMAL}"
python manage.py collectstatic --no-input

echo -e "${GREEN}Run server...${NORMAL}"
python3 -m gunicorn root.asgi:application -k uvicorn_worker.UvicornWorker -b 0.0.0.0:8000

echo -e "${GREEN}Server was stopped${NORMAL}"
