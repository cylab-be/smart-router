#!/bin/sh
#setup usb fs
opkg update
opkg install kmod-usb2 kmod-usb-storage kmod-fs-ext4 block-mount
if [ $(ls /mnt/ | grep -c "sda1") -eq 0 ] ; then :
	mkdir /mnt/sda1
	mount /dev/sda1 /mnt/sda1
	mkdir -p /tmp/cproot
	mount --bind / /tmp/cproot
	tar -C /tmp/cproot -cvf - . | tar -C /mnt/sda1 -xf -
	umount /tmp/cproot
fi


echo "config 'global'" > /etc/config/fstab
echo "	option	anon_swap	'0'" >> /etc/config/fstab
echo "	option	anon_mount	'0'" >> /etc/config/fstab
echo "	option	auto_swap	'1'" >> /etc/config/fstab
echo "	option	auto_mount	'1'" >> /etc/config/fstab
echo "	option	delay_root	'5'" >> /etc/config/fstab
echo "	option	check_fs	'0'" >> /etc/config/fstab
echo "" >> /etc/config/fstab
echo "config mount" >> /etc/config/fstab
echo "        option target        /" >> /etc/config/fstab
echo "        option device        /dev/sda1" >> /etc/config/fstab
echo "        option fstype        ext4" >> /etc/config/fstab
echo "        option options       rw,sync" >> /etc/config/fstab
echo "        option enabled       1" >> /etc/config/fstab
echo "        option enabled_fsck  0" >> /etc/config/fstab




