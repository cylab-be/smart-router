#!/bin/sh
sleep 5
mkdir .cache
cd /root/smart-router ; screen -dmS IDS sh -c 'python3 manage.py runserver 0.0.0.0:8000'