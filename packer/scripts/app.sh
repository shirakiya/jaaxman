#!/bin/bash
set -eu

cd $HOME

apt update

# Nginx
apt install -y nginx
NGINX_LOG_DIR=/var/log/nginx/jaaxman
mkdir $NGINX_LOG_DIR
chown root:root $NGINX_LOG_DIR
chmod -R 777 $NGINX_LOG_DIR

# uwsgi
UWSGI_LOG_DIR=/var/log/uwsgi
mkdir $UWSGI_LOG_DIR
chown root:root $UWSGI_LOG_DIR
chmod -R 777 $UWSGI_LOG_DIR

# MySQL
apt install -y libmysqlclient-dev
