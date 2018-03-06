#!/bin/sh

sudo apt-get install libc6-dev-i386
cd ~/src
git clone --recursive https://github.com/dmlc/mxnet
cd mxnet
cp make/config.mk .

echo "Edit ~/src/mxnet/config.mk"
echo "make -j4"
