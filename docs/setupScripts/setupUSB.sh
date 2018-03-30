#!/bin/sh
#setup usb fs

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

printf "${BLUE}[INFO] - Installing few tools ${NORMAL}\n" 
install_package "kmod-usb2"
install_package "kmod-usb-storage"
install_package "kmod-fs-ext4"
install_package "block-mount"
printf "${GREEN}[INFO] - few tools installed ${NORMAL}\n\n"


if [ $(ls /mnt/ | grep -c "sda1") -eq 0 ] ; then :
	printf "${BLUE}[INFO] - mouting usb stick and copy fhs ${NORMAL}\n" 
	mkdir /mnt/sda1
	mount /dev/sda1 /mnt/sda1
	mkdir -p /tmp/cproot
	mount --bind / /tmp/cproot
	tar -C /tmp/cproot -cvf - . | tar -C /mnt/sda1 -xf -
	umount /tmp/cproot
	printf "${GREEN}[INFO] - end of mouting operations ${NORMAL}\n\n"
else
	printf "${YELLOW}[WARNING] - /mnt/sda1 already existent, remove it to redo mounting operations ${NORMAL}\n" 
fi

if [ $(cat /etc/config/fstab | grep -c -i 'sda1') -eq 0 ] ; then :
	printf "${BLUE}[INFO] - editting /etc/config/fstab to run fhs from usb at startup ${NORMAL}\n" 
	# echo "config 'global'" > /etc/config/fstab
	# echo "	option	anon_swap	'0'" >> /etc/config/fstab
	# echo "	option	anon_mount	'0'" >> /etc/config/fstab
	# echo "	option	auto_swap	'1'" >> /etc/config/fstab
	# echo "	option	auto_mount	'1'" >> /etc/config/fstab
	# echo "	option	delay_root	'5'" >> /etc/config/fstab
	# echo "	option	check_fs	'0'" >> /etc/config/fstab
	# echo "" >> /etc/config/fstab
	echo "config mount" >> /etc/config/fstab
	echo "        option target        /" >> /etc/config/fstab
	echo "        option device        /dev/sda1" >> /etc/config/fstab
	echo "        option fstype        ext4" >> /etc/config/fstab
	echo "        option options       rw,sync" >> /etc/config/fstab
	echo "        option enabled       1" >> /etc/config/fstab
	echo "        option enabled_fsck  0" >> /etc/config/fstab
	echo "" >> /etc/config/fstab

	printf "${GREEN}[INFO] - USB settings OK ! ${NORMAL}\n\n"
	printf "${GREEN}[INFO] - You have now to ${RED} REBOOT ! ${NORMAL}\n\n"
else
	printf "${YELLOW}[WARNING] - /etc/mnt/fstab already existent, remove 'config mount' section to redo config ${NORMAL}\n" 
fi


