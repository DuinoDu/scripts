#!/bin/bash

if [ ! -d ~/opt ];then
    mkdir ~/opt
fi

cd /tmp
wget https://nodejs.org/dist/v9.6.1/node-v9.6.1-linux-x64.tar.xz
tar -xvf node-v9.6.1-linux-x64.tar.xz
mv node-v9.6.1-linux-x64 ~/opt/node

echo "NODE_PATH=$HOME/opt/node/lib/node_modules" >> ~/.zshrc
echo "PATH=$HOME/opt/node/bin:$PATH" >> ~/.zshrc
export NODE_PATH=$HOME/opt/node/lib/node_modules
export PATH=$HOME/opt/node/bin:$PATH

npm --registry https://registry.npm.taobao.org info underscore
npm install -g cnpm
