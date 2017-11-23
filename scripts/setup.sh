#!/bin/bash
set -eu

cd /root/jaaxman

# export Environment variables
aws s3 cp s3://jaaxman-production-infla/production-env /root/env
./scripts/export_env.sh

# setup app
/root/local/python-3.6.2/bin/pip install -f wheelhouse --no-index -r requirements.txt

if [ $DEPLOYMENT_GROUP_NAME = 'jaaxman-job' ]; then
  /root/local/python-3.6.2/bin/python manage.py migrate
fi
