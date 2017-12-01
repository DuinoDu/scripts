#!/bin/sh

sudo apt-get install mpi-default-dev libicu-dev python-dev libbz2-dev 
wget http://sources.webos-ports.org/boost_1_56_0.tar.bz2
tar -jxvf boost_1_56_0.tar.bz2
cd boost_1_56_0
chmod +x bootstrap.sh
./bootstrap.sh
./b2
sudo ./b2 install
