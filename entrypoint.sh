#!/bin/bash

echo "Enter to entrypoint"

pip install -r requirements/base.txt
python3 manage.py migrate bot
python3 manage.py run_bot
