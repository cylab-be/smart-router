#!/bin/sh

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NORMAL='\033[0m'

printf "${BLUE}[INFO] - Updating sources ${NORMAL}\n" 
opkg update
printf "${GREEN}[INFO] - sources updated ${NORMAL}\n\n"

# Divers
printf "${BLUE}[INFO] - Installing few tools ${NORMAL}\n" 
opkg install ca-bundle ca-certificates zsh curl git-http nano
printf "${GREEN}[INFO] - few tools installed ${NORMAL}\n\n"

#ntp client
printf "${BLUE}[INFO] - Installing ntp client ${NORMAL}\n" 
opkg install ntpd
/etc/init.d/sysntpd disable
/etc/init.d/ntpd enable
/etc/init.d/ntpd start
printf "${GREEN}[INFO] - ntp client installed and running ${NORMAL}\n\n"


#pkill
printf "${BLUE}[INFO] - Installing pkill ${NORMAL}\n" 
opkg install procps-ng-pkill
printf "${GREEN}[INFO] - pkill installed ${NORMAL}\n\n"

#htop
printf "${BLUE}[INFO] - Installing htop ${NORMAL}\n" 
opkg install htop
printf "${GREEN}[INFO] - htop installed ${NORMAL}\n\n"

#Slack
printf "${BLUE}[INFO] - Installing slackclient ${NORMAL}\n" 
pip3 install slackclient
printf "${GREEN}[INFO] - slackclient installed ${NORMAL}\n\n"

#Scapy
printf "${BLUE}[INFO] - Installing scapy ${NORMAL}\n" 
opkg upgrade tar wget
opkg install python tcpdump unzip
wget http://www.secdev.org/projects/scapy/files/scapy-latest.tar.gz
tar -xvf scapy-latest.tar.gz
cd scapy-2.1.0
python setup.py install
cd ..
rm -rf scapy*
printf "${GREEN}[INFO] - scapy installed ${NORMAL}\n\n"

#sqlite3 + python3
printf "${BLUE}[INFO] - Installing python3 + sqlite3 ${NORMAL}\n" 
opkg install sqlite3-cli python-sqlite3 python3 python3-pip python-pip
printf "${GREEN}[INFO] - python3 + sqlite3 installed ${NORMAL}\n\n"

#pip
printf "${BLUE}[INFO] - Installing python-dotenv + scapy-python3 ${NORMAL}\n" 
# pip install --upgrade pip
pip3 install python-dotenv
pip3 install scapy-python3
printf "${GREEN}[INFO] - python-dotenv + scapy-python3 installed ${NORMAL}\n\n"

#SmartRouter config
printf "${BLUE}[INFO] - Installing SmartRouter ${NORMAL}\n" 
cd /root
git clone https://github.com/RUCD/smart-router.git 
ln -s /root/smart-router/ /etc
cp smart-router/docs/init_script.sh /etc/init.d/smartrouter
chmod +x /etc/init.d/smartrouter
/etc/init.d/smartrouter enable
#TODO cp tempalte.env -> .env and addapt it 
printf "${GREEN}[INFO] - SmartRouter installed ${NORMAL}\n\n"

#web
# php7 php7-cgi php7-fastcgi php7-mod-iconv 
printf "${BLUE}[INFO] - Installing web server ${NORMAL}\n" 
opkg install lighttpd lighttpd-mod-cgi lighttpd-mod-access lighttpd-mod-fastcgi
mkdir /var/www
sed -i 's|"/var"|"/var/www"|' /etc/lighttpd/lighttpd.conf
sed -i 's|80|81|' /etc/lighttpd/lighttpd.conf
# sed -i 's|".erb" => "/usr/bin/eruby",|".erb" =>  "/usr/bin/eruby", ".php" =>"/usr/bin/php-cgi",|' /etc/lighttpd/conf.d/30-cgi.conf
# sed -i 's|doc_root = "/www"|doc_root = "/var/www"|' /etc/php.ini
/etc/init.d/lighttpd restart
/etc/init.d/lighttpd enable
mkdir /etc/smart-router/logs
touch /etc/smart-router/logs/alerts.txt
ln -s /root/smart-router/logs/alerts.txt /var/www
printf "${GREEN}[INFO] - web server installed ${NORMAL}\n\n"

#Ohmyzsh
# opkg update
printf "${BLUE}[INFO] - Installing ohmyzsh ${NORMAL}\n" 
printf "${YELLOW}[INFO] - PLEASE TYPE 'exit' AFTER OHMYZSH HAS FINISHED TO INSTALL TO FINISH THE INSTALL ${NORMAL}\n" 
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh) ; exit" 
sed -i -- 's/ash/zsh/g' /etc/passwd
sed -i -- 's/robbyrussell/agnoster/g' /root/.zshrc
sed -i "s/prompt_segment blue black '%~'/prompt_segment blue black '%c'/" ~/.oh-my-zsh/themes/agnoster.zsh-theme
source ~/.zshrc
printf "${GREEN}[INFO] - ohmyzsh installed ${NORMAL}\n\n"









