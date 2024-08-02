#!/bin/sh
sleep 5
cd /root/smart-router/src ; screen -dmS IDS sh -c 'python3 manage.py runserver 192.168.1.3:8000'