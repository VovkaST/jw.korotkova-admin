#!/bin/bash

echo -e "${GREEN}Apply migrations...${NORMAL}"
python3 manage.py migrate
echo -e "${GREEN}Migration applied!${NORMAL}\n"
