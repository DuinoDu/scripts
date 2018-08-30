#!/bin/bash -e

board=stm32f103-minimum

if [ ! -d ~/src/nuttxspace ];then
    mkdir ~/src/nuttxspace
fi
cd ~/src/nuttxspace

git clone https://bitbucket.org/nuttx/nuttx.git nuttx
git clone https://bitbucket.org/nuttx/tools.git tools
git clone https://bitbucket.org/nuttx/app.git

cd tools/kconfig-frontends
./configure
make
sudo make install

if [ `uname -s` = 'Darwin' ]; then # mac
    sudo update_dyld_shared_cache
else # ubuntu
    sudo ldconfig
fi

cd ../../nuttx/tools
if [ Darwin = 'Darwin' ]; then
    ./configure.sh -m $borad/nsh
else
    ./configure.sh $borad/nsh
fi

echo "cd ~/src/nuttxspace/nuttx and make menuconfig to config nuttx"
