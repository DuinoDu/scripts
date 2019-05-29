#!/bin/bash -e

cd ~/
mkdir src_libvips && cd src_libvips
wget https://github.com/libvips/libvips/releases/download/v8.8.0-rc2/vips-8.8.0-rc2.tar.gz
tar -zxvf vips-v8.8.0-rc2.tar.gz

prefix=`which node`/../../

cd libvips-8.8.0
./configure --prefix=$prefix
make
make install
echo "installed in $prefix "
