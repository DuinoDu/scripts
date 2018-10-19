#!/bin/bash -e

sudo apt-get install gcc-multilib default-jre
sudo apt-get install libc6:i386 libncurses5:i386 libstdc++6:i386

if [ ! -d ~/src ];then
    mkdir ~/src
fi
cd ~/src
git clone http://gitlab.hobot.cc/HBDK/hbdk_download.git
git clone http://gitlab.hobot.cc/HBDK/hbcc_testsuite.git 
cd hbdk_download 
make

echo "hbdk are installed in ${HOME}/src"
