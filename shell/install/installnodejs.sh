#!/bin/bash

version=6.14.3

export NVM_NODEJS_ORG_MIRROR=https://npm.taobao.org/mirrors/node
git clone https://github.com/creationix/nvm.git ~/.nvm
source ~/.nvm/nvm.sh
nvm install $version 
nvm_install_latest_npm
npm config set registry https://registry.npm.taobao.org
npm config get registry

echo "source ~/.nvm/nvm.sh" >> ~/.zshrc
