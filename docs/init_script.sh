#!/bin/sh /etc/rc.common
# SmartRouter
START=70
STOP=15

SERVICE_DAEMONIZE=1
SERVICE_WRITE_PID=1

start() {
        # commands to launch application
        logger "SMARTROUTER :  started"
		/usr/bin/python3 /etc/smart-router/python/main.py >> /var/log/smart-router-errors.log &
}

stop() {
        # commands to kill application
	logger "SMARTROUTER : killing next porcesses : $(pgrep -f smart-router)"
	pkill -f smart-router
	logger "SMARTROUTER : stoped"
}

restart() {
	stop
	start
}

boot () {
	sleep 60
	start
}