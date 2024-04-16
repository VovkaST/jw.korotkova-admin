#!/bin/bash
YELLOW="\033[1;33m"
GREEN="\033[0;32m"
NORMAL="\033[0m"

echo -e "${YELLOW}Running admin-panel${NORMAL}"

source ./compose/build.sh
source ./compose/migrations.sh

echo -e "${GREEN}Run bot...${NORMAL}"
python3 manage.py run_bot
echo -e "${GREEN}Bot was stopped${NORMAL}"
