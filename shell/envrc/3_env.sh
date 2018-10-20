#!/bin/bash
PWD=`pwd`
#sudo apt-get update -y
#sudo apt-get install cmake python-dev python-pip -y

# git
git config --global user.email "472365351duino@gmail.com"
git config --global user.name "duinodu"

homerc=~/.zshrc
if [ ! -f $homerc ];then
    homerc=~/.bashrc
fi
echo "PATH=\$PATH:\$HOME/project/scripts/shell:\$HOME/project/scripts/python" >> $homerc
