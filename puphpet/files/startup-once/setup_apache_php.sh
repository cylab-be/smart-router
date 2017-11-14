#!/usr/bin/env bash
sudo a2dismod worker
sudo a2enmod php7.1
sudo rm -rf /etc/apache2/sites-enabled/10-default_vhost_80.conf
sudo service apache2 restart