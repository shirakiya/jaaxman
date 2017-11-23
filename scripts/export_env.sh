#!/bin/bash
set -eu

ENVFILE=/root/env
source $ENVFILE
export $(cut -d = -f 1 ${ENVFILE})
