#!/bin/bash

echo -e "${GREEN}Compile messages...${NORMAL}"
python manage.py compilemessages -l ru -l en
echo -e "${GREEN}Messages compiled!${NORMAL}\n"
