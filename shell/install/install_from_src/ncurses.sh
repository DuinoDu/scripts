#!/bin/bash

wget http://ftp.gnu.org/pub/gnu/ncurses/ncurses-5.7.tar.gz
tar xzf ncurses-5.7.tar.gz
cd ncurses-5.7
./configure --prefix=$HOME/.local/ncurses
make
make install
ls -la $HOME/.local/ncurses
