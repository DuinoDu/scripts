#!/bin/bash

#sudo apt-get install tmux zsh curl

# install ncurses
wget ftp://invisible-island.net/ncurses/ncurses.tar.gz
tar -zxvf ncurses.tar.gz
cd ncurses
export CXXFLAGS=' -fPIC'
export CFLAGS=' -fPIC'
./configure --prefix=$HOME/.local --enable-shared
make
# Deduce environment information and build private terminfo tree
cd progs
./capconvert
cd ..


## install zsh from src
#wget -O zsh.tar.gz https://sourceforge.net/projects/zsh/files/latest/download
#mkdir zsh && tar -xvzf zsh.tar.gz -C zsh --strip-components 1
#cd zsh
#./configure --prefix=$HOME
#make
#make install
#
#
## oh-my-zsh
#sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
#
##chsh -s /bin/zsh
