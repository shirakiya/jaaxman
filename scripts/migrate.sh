#!/bin/bash
set -eu

if [ $DEPLOYMENT_GROUP_NAME = 'jaaxman-job' ]; then
  /root/local/python-3.6.2/bin/python manage.py migrate
fi
