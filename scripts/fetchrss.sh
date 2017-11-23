#!/bin/bash
set -eu

cd /root/jaaxman
./scripts/export_env.sh
 /root/local/python-3.6.2/bin/python manage.py fetchrss
