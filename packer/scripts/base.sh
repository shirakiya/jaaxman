#!/bin/bash

cd $HOME
echo $HOME
apt update

# Timezone (UTC -> JST)
timedatectl set-timezone Asia/Tokyo

# Firewall
ufw disable

# Base packages
apt install -y openssl awscli

# Python
# ref.) https://github.com/pyenv/pyenv/wiki/Common-build-problems#requirements
apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev

mkdir /root/local/
git clone https://github.com/tagomoris/xbuild.git /root/xbuild
/root/xbuild/python-install 3.6.2 /root/local/python-3.6.2

echo 'export PATH=$HOME/local/python-3.6.2/bin:$PATH' >> /root/.bashrc
