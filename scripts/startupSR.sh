#!/bin/sh
sleep 5
cd /root/smart-router ; screen -dmS IDS sh -c 'python3 manage.py runserver 0.0.0.0:8000'