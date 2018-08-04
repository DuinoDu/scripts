#!/bin/bash
# File              : ../install/installnodejs.sh
# Author            : duino <472365351duino@gmail.com>
# Date              : 04.08.2018
# Last Modified Date: 04.08.2018
# Last Modified By  : duino <472365351duino@gmail.com>

version=6.14.3

export NVM_NODEJS_ORG_MIRROR=https://npm.taobao.org/mirrors/node
git clone https://github.com/creationix/nvm.git ~/.nvm
source ~/.nvm/nvm.sh
nvm install $version 
nvm_install_latest_npm
npm config set registry https://registry.npm.taobao.org
npm config get registry

shrc=$HOME/.bashrc
if [ -f $HOME/.zshrc ];then
    shrc=$HOME/.zshrc
fi
echo "source ~/.nvm/nvm.sh" >> $shrc
