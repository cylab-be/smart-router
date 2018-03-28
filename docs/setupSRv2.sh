#!/bin/sh

# Use colors, but only if connected to a terminal, and that terminal
# supports them.
if which tput >/dev/null 2>&1; then
	ncolors=$(tput colors)
fi
if [ -t 1 ] && [ -n "$ncolors" ] && [ "$ncolors" -ge 8 ]; then
	RED="$(tput setaf 1)"
	GREEN="$(tput setaf 2)"
	YELLOW="$(tput setaf 3)"
	BLUE="$(tput setaf 4)"
	BOLD="$(tput bold)"
	NORMAL="$(tput sgr0)"
else
	RED=""
	GREEN=""
	YELLOW=""
	BLUE=""
	BOLD=""
	NORMAL=""
fi

opkg update

#ntp client
printf "${BLUE}[INFO] - Installing ntp client ${NORMAL}" 
opkg install ntpd
/etc/init.d/sysntpd disable
/etc/init.d/ntpd enable
/etc/init.d/ntpd start
printf "${GREEN}[INFO] - ntp client Insatlled and running ${NORMAL}"


#pkill
printf "${BLUE}[INFO] - Installing pkill ${NORMAL}" 
opkg install procps-ng-pkill
printf "${GREEN}[INFO] - pkill Insatlled ${NORMAL}"

#htop
printf "${BLUE}[INFO] - Installing htop ${NORMAL}" 
opkg install htop
printf "${GREEN}[INFO] - htop Insatlled ${NORMAL}"

#Slack
printf "${BLUE}[INFO] - Installing slackclient ${NORMAL}" 
pip3 install slackclient
printf "${GREEN}[INFO] - slackclient Insatlled ${NORMAL}"

#Scapy
printf "${BLUE}[INFO] - Installing scapy ${NORMAL}" 
opkg upgrade tar wget
opkg install python tcpdump unzip
wget http://www.secdev.org/projects/scapy/files/scapy-latest.tar.gz
tar -xvf scapy-latest.tar.gz
cd scapy-2.1.0
python setup.py install
cd ..
rm -rf scapy*
printf "${GREEN}[INFO] - scapy Insatlled ${NORMAL}"

#sqlite3 + python3
printf "${BLUE}[INFO] - Installing python3 + sqlite3 ${NORMAL}" 
opkg install sqlite3-cli python-sqlite3 python3 python3-pip python-pip
printf "${GREEN}[INFO] - python3 + sqlite3 Insatlled ${NORMAL}"

#pip
printf "${BLUE}[INFO] - Installing python-dotenv + scapy-python3 ${NORMAL}" 
# pip install --upgrade pip
pip3 install python-dotenv
pip3 install scapy-python3
printf "${GREEN}[INFO] - python-dotenv + scapy-python3 Insatlled ${NORMAL}"

#SmartRouter config
printf "${BLUE}[INFO] - Installing SmartRouter ${NORMAL}" 
cd /root
git clone https://github.com/RUCD/smart-router.git 
ln -s /root/smart-router/ /etc
cp smart-router/docs/init_script.sh /etc/init.d/smartrouter
chmod +x /etc/init.d/smartrouter
/etc/init.d/smartrouter enable
#TODO cp tempalte.env -> .env and addapt it 
printf "${GREEN}[INFO] - SmartRouter Insatlled ${NORMAL}"

#web
# php7 php7-cgi php7-fastcgi php7-mod-iconv 
printf "${BLUE}[INFO] - Installing web server ${NORMAL}" 
opkg install lighttpd lighttpd-mod-cgi lighttpd-mod-access lighttpd-mod-fastcgi
mkdir /var/www
sed -i 's|"/var"|"/var/www"|' /etc/lighttpd/lighttpd.conf
sed -i 's|80|81|' /etc/lighttpd/lighttpd.conf
# sed -i 's|".erb" => "/usr/bin/eruby",|".erb" =>  "/usr/bin/eruby", ".php" =>"/usr/bin/php-cgi",|' /etc/lighttpd/conf.d/30-cgi.conf
sed -i 's|doc_root = "/www"|doc_root = "/var/www"|' /etc/php.ini
/etc/init.d/lighttpd restart
/etc/init.d/lighttpd enable
touch /etc/smart-router/logs/alerts.txt
ln -s /root/smart-router/logs/alerts.txt /var/www
printf "${GREEN}[INFO] - web server Insatlled ${NORMAL}"

#Ohmyzsh
# opkg update
printf "${BLUE}[INFO] - Installing ohmyzsh ${NORMAL}" 
opkg install ca-bundle ca-certificates zsh curl git-http nano
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh) ; exit" 
sed -i -- 's/ash/zsh/g' /etc/passwd
sed -i -- 's/robbyrussell/agnoster/g' /root/.zshrc
sed -i "s/prompt_segment blue black '%~'/prompt_segment blue black '%c'/" ~/.oh-my-zsh/themes/agnoster.zsh-theme
source ~/.zshrc









