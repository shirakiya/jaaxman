#!/bin/bash
set -eu

cd $HOME

# update ssh config
echo -e "\npython /opt/fetch_hosts.py\n" >> $HOME/.bash_profile
