#!/bin/bash
echo -e "${GREEN}Install system packages...${NORMAL}"
apt update -y
apt install gettext -y
echo -e "${GREEN}Packages installed!${NORMAL}\n"

echo -e "${GREEN}Install requirements...${NORMAL}"
pip install -r requirements/base.txt
echo -e "${GREEN}Requirements installed!${NORMAL}\n"
