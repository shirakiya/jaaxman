#!/bin/bash
set -eu

cd $HOME

apt-get update

# crontab
CRON_LOG_DIR=/var/log/jaaxman
mkdir $CRON_LOG_DIR
chmod -R 777 $CRON_LOG_DIR

crontab /root/crontab

systemctl enable cron
systemctl enable td-agent
