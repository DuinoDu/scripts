#!/bin/bash -e

sudo apt-get install make python-dev gcc-multilib default-jre
sudo apt-get install libc6:i386 libncurses5:i386 libstdc++6:i386

root=~/src
if [ ! -d $root ];then
    mkdir -p $root
fi
cd $root
git clone http://gitlab.hobot.cc/HBDK/hbdk_download.git
git clone http://gitlab.hobot.cc/HBDK/hbcc_testsuite.git 
cd hbdk_download 
make

homerc=~/.zshrc
if [ ! -f $homerc ];then
    homerc=~/.bashrc
fi
echo "export PATH=\$PATH:\$root/hbdk_download/bin" >> $homerc
echo "hbdk are installed in ${HOME}/src"
