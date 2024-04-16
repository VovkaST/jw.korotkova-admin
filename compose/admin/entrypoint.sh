#!/bin/bash
YELLOW="\033[1;33m"
GREEN="\033[0;32m"
NORMAL="\033[0m"

echo -e "${YELLOW}Running admin-panel${NORMAL}"

source /app/compose/build.sh
source /app/compose/migrations.sh

echo -e "${GREEN}Run server...${NORMAL}"
python3 manage.py runserver 0.0.0.0:8000
echo -e "${GREEN}Server was stopped${NORMAL}"
