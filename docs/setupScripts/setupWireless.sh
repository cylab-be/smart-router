#!/bin/sh
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NORMAL='\033[0m'

printf "${BLUE}[INFO] - Configuring wirelless settings ${NORMAL}\n" 
sed -i "/option disabled '1'/d" /etc/config/wireless
HOSTNAME=$(cat /etc/config/system |grep -i hostname | awk -F "'" '{print $2}')
sed -i "s/LEDE/$HOSTNAME/" /etc/config/wireless
sed -i "s/encryption 'none'/encryption 'psk-mixed'/" /etc/config/wireless
PASSWORD=$(strings /dev/urandom | grep -o '[[:alnum:]]' | head -n 30 | tr -d '\n'; echo)
sed -i "/option encryption 'psk-mixed'/a option key '$PASSWORD'" /etc/config/wireless
sed -i "s/option key/\\toption key/" /etc/config/wireless
sed -i "s/HT20/HT40/" /etc/config/wireless

printf "${GREEN}[INFO] - Configuring wireless settings ${NORMAL}\n" 
printf "${GREEN}[INFO] - SSID is $HOSTNAME and password is $PASSWORD, you can change it into LuCi interface ${NORMAL}\n" 

/etc/init.d/network reload
