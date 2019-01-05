#!/bin/bash
set -eu

ENVFILE=/root/env
source $ENVFILE
export $(cut -d = -f 1 ${ENVFILE})

cd /root/jaaxman/backend
/root/local/python-3.6.2/bin/python manage.py fetchrss
