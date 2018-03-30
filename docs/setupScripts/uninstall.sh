#!/bin/sh

sed -i -- 's/zsh/ash/g' /etc/passwd
rm -rf /var/www
rm -rf /root/smart-router
rm -rf /etc/smart-router
rm -rf /etc/init.d/smartrouter
rm -rf /root/.oh-my-zsh
opkg remove --force-remove --force-removal-of-dependent-packages ca-bundle ca-certificates zsh curl git-http nano ntpd procps-ng-pkill htop python tcpdump unzip sqlite3-cli python-sqlite3 python3 python3-pip python-pip lighttpd lighttpd-mod-cgi lighttpd-mod-access lighttpd-mod-fastcgi

