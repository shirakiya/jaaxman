#!/bin/bash
set -eu

/root/local/python-3.6.2/bin/pip install -f wheelhouse --no-index -r requirements.txt

if [ $DEPLOYMENT_GROUP_NAME = 'jaaxman-job' ]; then
  /root/local/python-3.6.2/bin/python manage.py migrate
fi
