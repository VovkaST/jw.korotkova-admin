#!/bin/bash
YELLOW="\033[1;33m"
GREEN="\033[0;32m"
NORMAL="\033[0m"

echo -e "${YELLOW}Running Celery beat${NORMAL}"

source ./compose/migrations.sh
source ./compose/make_messages.sh

echo -e "${GREEN}Run Celery...${NORMAL}"
celery -A root.tasks worker -B --loglevel=INFO
echo -e "${GREEN}Celery was stopped${NORMAL}"
