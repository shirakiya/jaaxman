#!/bin/bash
set -eu

cd $HOME
echo $HOME
apt-get update

# Timezone (UTC -> JST)
timedatectl set-timezone Asia/Tokyo

# Firewall
ufw disable

# Base packages
apt-get install -y openssl awscli

# NTP
apt-get install -y ntp
sed -e 's/ubuntu.pool.ntp.org iburst/amazon.pool.ntp.org/' /etc/ntp.conf
timedatectl
systemctl enable ntp

# fluentd
cat << EOS >> /etc/security/limits.conf
root soft nofile 65536
root hard nofile 65536
* soft nofile 65536
* hard nofile 65536
EOS

curl -L https://toolbelt.treasuredata.com/sh/install-ubuntu-xenial-td-agent2.sh | sh
sed -i -e '14a export AWS_REGION=ap-northeast-1' /etc/init.d/td-agent


# Python
# ref.) https://github.com/pyenv/pyenv/wiki/Common-build-problems#requirements
apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev

mkdir /root/local/
git clone https://github.com/tagomoris/xbuild.git /root/xbuild
/root/xbuild/python-install 3.6.2 /root/local/python-3.6.2

echo 'export PATH=$HOME/local/python-3.6.2/bin:$PATH' >> /root/.bashrc

# MySQL
apt-get install -y libmysqlclient-dev mysql-client
