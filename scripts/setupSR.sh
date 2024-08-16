#!/bin/sh

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NORMAL='\033[0m'

ALREADY_INSTALLED="is up to date"
CANNOT_INSTALL="Cannot"


install_package () {
	printf "${BLUE}[INFO] - installing $1 ... ${NORMAL}\n\n"
	OUT=$(opkg install $1 2>&1)
	if [ $(echo $OUT | grep -i -c "$ALREADY_INSTALLED" ) -eq 1 ] ; then
		printf "${YELLOW}[WARNING] - $1 already installed${NORMAL}\n\n"
	else
		if [ $(echo $OUT | grep -i -c "$CANNOT_INSTALL") -eq 1 ] ; then
			echo $OUT
			printf "${RED}[ERROR] - cannot install $1${NORMAL}\n\n"
		else
			printf "${GREEN}[INFO] - $1 installed${NORMAL}\n\n"
		fi
	fi
}

printf "${BLUE}[INFO] - Updating sources ${NORMAL}\n"
opkg update
opkg upgrade tar wget
printf "${GREEN}[INFO] - sources updated ${NORMAL}\n\n"

# Divers
printf "${BLUE}[INFO] - Installing few tools ${NORMAL}\n"
install_package "git-http"
install_package "screen"
install_package "openssh-sftp-server"
printf "${GREEN}[INFO] - few tools installed ${NORMAL}\n\n"

#Snort
printf "${BLUE}[INFO] - Installing snort ${NORMAL}\n"
install_package "snort"
mkdir /usr/lib/snort_dynamicrules
printf "${GREEN}[INFO] - snort installed ${NORMAL}\n\n"

#Python3 (Django, scapy)
printf "${BLUE}[INFO] - Installing python3 and some packages ${NORMAL}\n"
install_package "python3"
install_package "python3-pip"
python3 -m pip install -r requirements.txt
printf "${GREEN}[INFO] - Installing python3 and some packages ${NORMAL}\n\n"

#SmartRouter config
printf "${BLUE}[INFO] - Installing SmartRouter ${NORMAL}\n"
git clone https://gitlab.cylab.be/cylab/smart-router.git
cd smart-router
git checkout v2
# copy snort.conf
cp tools/snort/snort.conf /etc/snort/snort.conf
# copy rules folder
cp -r tools/snort/rules /etc/snort/
printf "${GREEN}[INFO] - SmartRouter installed ${NORMAL}\n\n"

#web
printf "${BLUE}[INFO] - Installing web server ${NORMAL}\n"
python3 manage.py makemigrations dashboard
python3 manage.py migrate
screen -dmS IDS sh -c 'python3 manage.py runserver 192.168.1.3:8000'
printf "${GREEN}[INFO] - web server installed ${NORMAL}\n\n"

#Auto start after reboot
printf "${BLUE}[INFO] - Configure auto startup after reboot ${NORMAL}\n"
cp /root/smart-router/scripts/rc.local /etc/rc.local
chmod +x /root/smart-router/scripts/startupSR.sh
printf "${GREEN}[INFO] - Auto startup configured ${NORMAL}\n\n"