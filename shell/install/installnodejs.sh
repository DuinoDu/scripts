#!/bin/bash

export NVM_NODEJS_ORG_MIRROR=https://npm.taobao.org/mirrors/node
git clone https://github.com/creationix/nvm.git ~/.nvm
source ~/.nvm/nvm.sh
nvm install 4.7.0
nvm_install_latest_npm
npm config set registry https://registry.npm.taobao.org
npm config get registry

echo "source ~/.nvm/nvm.sh" >> .zshrc
