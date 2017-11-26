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

if [ $DEPLOYMENT_GROUP_NAME = 'jaaxman-job' ]; then
  /root/local/python-3.6.2/bin/python manage.py migrate
  /root/local/python-3.6.2/bin/python manage.py registerrss
fi
