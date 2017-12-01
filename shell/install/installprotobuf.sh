#!/bin/sh

sudo apt-get install -y autoconf automake libtool curl make g++ unzip

cd ~/src
git clone https://github.com/google/protobuf
cd protobuf
./autogen.sh

make && \
sudo make install && \
sudo ldconfig
