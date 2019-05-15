#!/bin/bash -e

cd ~/
mkdir src_libvips && cd src_libvips
wget https://github.com/libvips/libvips/releases/download/v8.8.0-rc2/vips-8.8.0-rc2.tar.gz
tar -zxvf vips-v8.8.0-rc2.tar.gz

cd libvips-8.8.0
./configure
make
