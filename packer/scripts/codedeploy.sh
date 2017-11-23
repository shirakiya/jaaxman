#!/bin/bash
set -eu
cd $HOME

apt-get update

# install CodeDeploy agent
apt-get install -y ruby wget
wget https://aws-codedeploy-ap-northeast-1.s3.amazonaws.com/latest/install
chmod +x install
./install auto
