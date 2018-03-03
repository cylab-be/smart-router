#!/bin/sh /etc/rc.common
# SmartRouter
START=60
STOP=15

start() {
        echo start
	/usr/bin/python3 /root/smart-router/python/main.py >> /root/smart-router/logs/errors.log &
        # commands to launch application
}

stop() {
        echo stop
	/usr/bin/killall python3
        # commands to kill application
}

restart() {
	stop
	start
}

boot() {
	start_service
}