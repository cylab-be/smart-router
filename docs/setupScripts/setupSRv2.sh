#!/bin/sh

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NORMAL='\033[0m'

ALREADY_INSTALLED="is up to date"

printf "${BLUE}[INFO] - Updating sources ${NORMAL}\n" 
opkg update
printf "${GREEN}[INFO] - sources updated ${NORMAL}\n\n"

# Divers
printf "${BLUE}[INFO] - Installing few tools ${NORMAL}\n" 
if [ $(opkg install ca-bundle | grep -i -c $ALREADY_INSTALLED ) -gt 0 ] ; then 
	printf "${YELLOW}[INFO] - ca-bundle already installed${NORMAL}\n\n"
else 
	printf "${GREEN}[INFO] - ca-bundle installed${NORMAL}\n\n"
fi
if [ $(opkg install ca-certificates | grep -i -c $ALREADY_INSTALLED ) -gt 0 ] ; then 
	printf "${YELLOW}[INFO] - ca-certificates already installed${NORMAL}\n\n"
else 
	printf "${GREEN}[INFO] - ca-certificates installed${NORMAL}\n\n"
fi
if [ $(opkg install zsh | grep -i -c $ALREADY_INSTALLED ) -gt 0 ] ; then 
	printf "${YELLOW}[INFO] - zsh already installed${NORMAL}\n\n"
else 
	printf "${GREEN}[INFO] - zsh installed${NORMAL}\n\n"
fi
if [ $(opkg install curl | grep -i -c $ALREADY_INSTALLED ) -gt 0 ] ; then 
	printf "${YELLOW}[INFO] - curl already installed${NORMAL}\n\n"
else 
	printf "${GREEN}[INFO] - curl installed${NORMAL}\n\n"
fi
if [ $(opkg install git-http | grep -i -c $ALREADY_INSTALLED ) -gt 0 ] ; then 
	printf "${YELLOW}[INFO] - git-http already installed${NORMAL}\n\n"
else 
	printf "${GREEN}[INFO] - git-http installed${NORMAL}\n\n"
fi
if [ $(opkg install nano | grep -i -c $ALREADY_INSTALLED ) -gt 0 ] ; then 
	printf "${YELLOW}[INFO] - nano already installed${NORMAL}\n\n"
else 
	printf "${GREEN}[INFO] - nano installed${NORMAL}\n\n"
fi
if [ $(opkg install htop | grep -i -c $ALREADY_INSTALLED ) -gt 0 ] ; then 
	printf "${YELLOW}[INFO] - htop already installed${NORMAL}\n\n"
else 
	printf "${GREEN}[INFO] - htop installed${NORMAL}\n\n"
fi
if [ $(opkg install slackclient | grep -i -c $ALREADY_INSTALLED ) -gt 0 ] ; then 
	printf "${YELLOW}[INFO] - slackclient already installed${NORMAL}\n\n"
else 
	printf "${GREEN}[INFO] - slackclient installed${NORMAL}\n\n"
fi
if [ $(opkg install procps-ng-pkill | grep -i -c $ALREADY_INSTALLED ) -gt 0 ] ; then 
	printf "${YELLOW}[INFO] - procps-ng-pkill already installed${NORMAL}\n\n"
else 
	printf "${GREEN}[INFO] - procps-ng-pkill installed${NORMAL}\n\n"
fi



printf "${GREEN}[INFO] - few tools installed ${NORMAL}\n\n"

#ntp client
printf "${BLUE}[INFO] - Installing ntp client ${NORMAL}\n" 
if [ $(opkg install ntpd | grep -i -c $ALREADY_INSTALLED ) -gt 0 ] ; then 
	printf "${YELLOW}[INFO] - ntpd already installed${NORMAL}\n\n"
else 
	printf "${GREEN}[INFO] - ntpd installed${NORMAL}\n\n"
fi

/etc/init.d/sysntpd disable
/etc/init.d/ntpd enable
/etc/init.d/ntpd start
printf "${GREEN}[INFO] - ntp client installed and running ${NORMAL}\n\n"


#Scapy
printf "${BLUE}[INFO] - Installing scapy ${NORMAL}\n" 
opkg upgrade tar wget
if [ $(opkg install python | grep -i -c $ALREADY_INSTALLED ) -gt 0 ] ; then 
	printf "${YELLOW}[INFO] - python already installed${NORMAL}\n\n"
else 
	printf "${GREEN}[INFO] - python installed${NORMAL}\n\n"
fi
if [ $(opkg install tcpdump | grep -i -c $ALREADY_INSTALLED ) -gt 0 ] ; then 
	printf "${YELLOW}[INFO] - tcpdump already installed${NORMAL}\n\n"
else 
	printf "${GREEN}[INFO] - tcpdump installed${NORMAL}\n\n"
fi
if [ $(opkg install unzip | grep -i -c $ALREADY_INSTALLED ) -gt 0 ] ; then 
	printf "${YELLOW}[INFO] - unzip already installed${NORMAL}\n\n"
else 
	printf "${GREEN}[INFO] - unzip installed${NORMAL}\n\n"
fi
wget http://www.secdev.org/projects/scapy/files/scapy-latest.tar.gz
tar -xvf scapy-latest.tar.gz
cd scapy-2.1.0
python setup.py install
cd ..
rm -rf scapy*
printf "${GREEN}[INFO] - scapy installed ${NORMAL}\n\n"

#sqlite3 + python3
printf "${BLUE}[INFO] - Installing python3 + sqlite3 ${NORMAL}\n" 
if [ $(opkg install sqlite3-cli | grep -i -c $ALREADY_INSTALLED ) -gt 0 ] ; then 
	printf "${YELLOW}[INFO] - sqlite3-cli already installed${NORMAL}\n\n"
else 
	printf "${GREEN}[INFO] - sqlite3-cli installed${NORMAL}\n\n"
fi
if [ $(opkg install python-sqlite3 | grep -i -c $ALREADY_INSTALLED ) -gt 0 ] ; then 
	printf "${YELLOW}[INFO] - python-sqlite3 already installed${NORMAL}\n\n"
else 
	printf "${GREEN}[INFO] - python-sqlite3 installed${NORMAL}\n\n"
fi
if [ $(opkg install python3 | grep -i -c $ALREADY_INSTALLED ) -gt 0 ] ; then 
	printf "${YELLOW}[INFO] - python3 already installed${NORMAL}\n\n"
else 
	printf "${GREEN}[INFO] - python3 installed${NORMAL}\n\n"
fi
if [ $(opkg install python3-pip | grep -i -c $ALREADY_INSTALLED ) -gt 0 ] ; then 
	printf "${YELLOW}[INFO] - python3-pip already installed${NORMAL}\n\n"
else 
	printf "${GREEN}[INFO] - python3-pip installed${NORMAL}\n\n"
fi
if [ $(opkg install python-pip | grep -i -c $ALREADY_INSTALLED ) -gt 0 ] ; then 
	printf "${YELLOW}[INFO] - python-pip already installed${NORMAL}\n\n"
else 
	printf "${GREEN}[INFO] - python-pip installed${NORMAL}\n\n"
fi
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
if [ $(opkg install lighttpd | grep -i -c $ALREADY_INSTALLED ) -gt 0 ] ; then 
	printf "${YELLOW}[INFO] - lighttpd already installed${NORMAL}\n\n"
else 
	printf "${GREEN}[INFO] - lighttpd installed${NORMAL}\n\n"
fi
if [ $(opkg install lighttpd-mod-cgi | grep -i -c $ALREADY_INSTALLED ) -gt 0 ] ; then 
	printf "${YELLOW}[INFO] - lighttpd-mod-cgi already installed${NORMAL}\n\n"
else 
	printf "${GREEN}[INFO] - lighttpd-mod-cgi installed${NORMAL}\n\n"
fi
if [ $(opkg install lighttpd-mod-access | grep -i -c $ALREADY_INSTALLED ) -gt 0 ] ; then 
	printf "${YELLOW}[INFO] - lighttpd-mod-access already installed${NORMAL}\n\n"
else 
	printf "${GREEN}[INFO] - lighttpd-mod-access installed${NORMAL}\n\n"
fi
if [ $(opkg install lighttpd-mod-fastcgi | grep -i -c $ALREADY_INSTALLED ) -gt 0 ] ; then 
	printf "${YELLOW}[INFO] - lighttpd-mod-fastcgi already installed${NORMAL}\n\n"
else 
	printf "${GREEN}[INFO] - lighttpd-mod-fastcgi installed${NORMAL}\n\n"
fi

mkdir /var/www
sed -i 's|"/var"|"/var/www"|' /etc/lighttpd/lighttpd.conf
sed -i 's|80|81|' /etc/lighttpd/lighttpd.conf
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









