#!/bin/bash
set -eu

systemctl enable nginx
systemctl enable td-agent
systemctl enable uwsgi
