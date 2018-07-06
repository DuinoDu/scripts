#!/bin/bash -ex

prefix=$HOME/.local

cd /tmp
wget https://prdownloads.sourceforge.net/tcl/tcl8.6.8-src.tar.gz
tar -zxvf tcl8.6.8-src.tar.gz
cd tcl8.6.8/unix

./configure --prefix=$prefix --exec-prefix=$prefix
make -j4
make install

echo "Not complete, only install tcl, not tkinter"
