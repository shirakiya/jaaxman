#!/bin/bash
set -eu

# export Environment variables
ENVFILE=/root/env
aws s3 cp s3://jaaxman-production-infla/production-env $ENVFILE
source $ENVFILE
export $(cut -d = -f 1 ${ENVFILE})

# setup app
cd /root/jaaxman
/root/local/python-3.6.2/bin/pip install -f wheelhouse --no-index -r requirements.txt
# workaround
# ref.) https://stackoverflow.com/questions/36796167/upgraded-to-ubuntu-16-04-now-mysql-python-dependencies-are-broken
/root/local/python-3.6.2/bin/pip uninstall -y mysqlclient
/root/local/python-3.6.2/bin/pip install --no-binary mysqlclient mysqlclient==1.3.12
/root/local/python-3.6.2/bin/pip uninstall -y uWSGI
/root/local/python-3.6.2/bin/pip install uWSGI


if [ $DEPLOYMENT_GROUP_NAME = 'jaaxman-job' ]; then
  /root/local/python-3.6.2/bin/python manage.py migrate
  /root/local/python-3.6.2/bin/python manage.py registerrss
elif [ $DEPLOYMENT_GROUP_NAME = 'jaaxman-app' ]; then
  systemctl restart uwsgi
fi
