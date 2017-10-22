#!/bin/bash
set -eu

systemctl enable nginx
systemctl enable uwsgi
