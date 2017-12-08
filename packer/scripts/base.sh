#!/bin/bash
set -eu

# Timezone
setup_timezone () {
  # UTC -> JST
  timedatectl set-timezone Asia/Tokyo
}

# Firewall
setup_firewall () {
  ufw disable
}

# Base packages
setup_base_packages () {
  apt-get install -y openssl awscli

  # MySQL
  apt-get install -y libmysqlclient-dev mysql-client
}

# NTP
setup_ntp () {
  apt-get install -y ntp
  sed -e 's/ubuntu.pool.ntp.org iburst/amazon.pool.ntp.org/' /etc/ntp.conf
  timedatectl
  systemctl enable ntp
}

# Fluentd
setup_fluentd () {
  cat << EOS >> /etc/security/limits.conf
root soft nofile 65536
root hard nofile 65536
* soft nofile 65536
* hard nofile 65536
EOS

  curl -L https://toolbelt.treasuredata.com/sh/install-ubuntu-xenial-td-agent2.sh | sh
  sed -i -e '14a export AWS_REGION=ap-northeast-1' /etc/init.d/td-agent

  # fluent-plugin-cloudwatch-logs
  # https://github.com/ryotarai/fluent-plugin-cloudwatch-logs
  /opt/td-agent/embedded/bin/gem install fluent-plugin-cloudwatch-logs --no-ri --no-rdoc
}

# Mackerel
setup_mackerel () {
  wget -q -O - https://mackerel.io/file/script/setup-apt-v2.sh | sh
  sudo apt-get install -y mackerel-agent
  mkdir /etc/mackerel-agent/conf.d
  cat << EOS > /etc/mackerel-agent/mackerel-agent.conf
apikey = "${MACKEREL_APIKEY}"
include = "/etc/mackerel-agent/conf.d/*.conf"
EOS
  systemctl enable mackerel-agent
}

# Python
# ref.) https://github.com/pyenv/pyenv/wiki/Common-build-problems#requirements
setup_python () {
  apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev
  mkdir /root/local/
  git clone https://github.com/tagomoris/xbuild.git /root/xbuild
  /root/xbuild/python-install 3.6.2 /root/local/python-3.6.2
  echo -e "export PATH=$HOME/local/python-3.6.2/bin:$PATH\n" >> /root/.bash_profile
}


cd $HOME
echo $HOME
apt-get update

setup_timezone
setup_firewall
setup_base_packages
setup_ntp
setup_fluentd
setup_mackerel
setup_python
