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
printf "${GREEN}[INFO] - sources updated ${NORMAL}\n\n"

# Divers
printf "${BLUE}[INFO] - Installing few tools ${NORMAL}\n" 
install_package "ca-bundle"
install_package "ca-certificates"
install_package "zsh"
install_package "curl"
install_package "git-http"
install_package "nano"
install_package "htop"
install_package "procps-ng-pkill"
install_package "ntpd"
printf "${GREEN}[INFO] - few tools installed ${NORMAL}\n\n"

#ntp client
/etc/init.d/sysntpd disable
/etc/init.d/ntpd enable
/etc/init.d/ntpd start
printf "${GREEN}[INFO] - ntp client installed and running ${NORMAL}\n\n"


#Scapy
printf "${BLUE}[INFO] - Installing scapy ${NORMAL}\n" 
opkg upgrade tar wget
install_package "python"
install_package "tcpdump"
install_package "unzip"
wget http://www.secdev.org/projects/scapy/files/scapy-latest.tar.gz
tar -xvf scapy-latest.tar.gz
cd scapy-2.1.0
python setup.py install
cd ..
rm -rf scapy*
printf "${GREEN}[INFO] - scapy installed ${NORMAL}\n\n"

#sqlite3 + python3
printf "${BLUE}[INFO] - Installing python3 + sqlite3 ${NORMAL}\n" 
install_package "sqlite3-cli"
install_package "python-sqlite3"
install_package "python3"
install_package "python3-pip"
install_package "python-pip"
printf "${GREEN}[INFO] - python3 + sqlite3 installed ${NORMAL}\n\n"

#pip
printf "${BLUE}[INFO] - Installing python-dotenv + scapy-python3 ${NORMAL}\n" 
pip3 install python-dotenv
pip3 install scapy-python3
printf "${GREEN}[INFO] - python-dotenv + scapy-python3 installed ${NORMAL}\n\n"

#slackclient
printf "${BLUE}[INFO] - Installing slackclient ${NORMAL}\n" 
pip3 install slackclient
printf "${GREEN}[INFO] - slackclient installed ${NORMAL}\n\n"

#SmartRouter config
printf "${BLUE}[INFO] - Installing SmartRouter ${NORMAL}\n" 
cd /root
git clone https://github.com/RUCD/smart-router.git 
ln -s /root/smart-router/ /etc
cp smart-router/docs/init_script.sh /etc/init.d/smartrouter
chmod +x /etc/init.d/smartrouter
/etc/init.d/smartrouter enable
cp smart-router/docs/template.env smart-router/python/.env
IGNORED_MAC_ADDRESS=$(ifconfig | grep -i HW | awk -F " " '{print $5}' | awk '{printf "%s,",$0} END {print ""}')
IGNORED_MAC_ADDRESS=$(echo "${IGNORED_MAC_ADDRESS%?}")
sed -i "s/IGNORED_MAC=/IGNORED_MAC=$IGNORED_MAC_ADDRESS/" smart-router/python/.env
printf "${GREEN}[INFO] - SmartRouter installed ${NORMAL}\n\n"

#web
# php7 php7-cgi php7-fastcgi php7-mod-iconv 
printf "${BLUE}[INFO] - Installing web server ${NORMAL}\n" 
install_package "lighttpd"
install_package "lighttpd-mod-cgi"
install_package "lighttpd-mod-access"
install_package "lighttpd-mod-fastcgi"
mkdir /var/www
sed -i 's|"/var"|"/var/www"|' /etc/lighttpd/lighttpd.conf
sed -i 's|80|81|' /etc/lighttpd/lighttpd.conf
sed -i 's/#server.port/server.port/' /etc/lighttpd/lighttpd.conf
ed -i 's|"/www"|"/var/www"|' /etc/lighttpd/lighttpd.conf
/etc/init.d/lighttpd restart
/etc/init.d/lighttpd enable
mkdir /etc/smart-router/logs
echo "Temporary alerts file" >> /etc/smart-router/logs/alerts.txt
ln -s /root/smart-router/logs/alerts.txt /var/www
printf "${GREEN}[INFO] - web server installed ${NORMAL}\n\n"


#Ohmyzsh
printf "${BLUE}[INFO] - Installing ohmyzsh ${NORMAL}\n" 
printf "${YELLOW}[INFO] - PLEASE TYPE 'exit' AFTER OHMYZSH HAS FINISHED TO INSTALL TO FINISH THE INSTALL ${NORMAL}\n" 
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh) ; exit" 
sed -i -- 's/ash/zsh/g' /etc/passwd
sed -i -- 's/robbyrussell/agnoster/g' /root/.zshrc
sed -i "s/prompt_segment blue black '%~'/prompt_segment blue black '%c'/" ~/.oh-my-zsh/themes/agnoster.zsh-theme
zsh -c "source ~/.zshrc"
printf "${GREEN}[INFO] - ohmyzsh installed ${NORMAL}\n\n"

printf "${BLUE}[INFO] - starting smart-router ... ${NORMAL}\n\n"
/etc/init.d/smartrouter start
printf "${GREEN}[INFO] - smart-router started ${NORMAL}\n\n"

printf "${GREEN}[INFO] - do no forgive to edit /etc/smart-router/python/.env file for more customisation (slack notifications etc.) ${NORMAL}\n\n"
printf "${YELLOW}[WARNING] - In case you edit the /etc/smart-router/python/.env, do not forget to restart SR (/etc/init.d/smartrouter restart)${NORMAL}\n\n"









