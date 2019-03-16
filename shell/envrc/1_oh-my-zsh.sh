#!/bin/bash -ex

#sudo apt-get install tmux zsh curl

# oh-my-zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

# oh-my-zsh plugin
ZSH_CUSTOM=/home/duino/.oh-my-zsh/custom
git clone git://github.com/zsh-users/zsh-autosuggestions $ZSH_CUSTOM/plugins/zsh-autosuggestions

# oh-my-zsh plugin
#sudo apt install zsh-syntax-highlighting
#rm ~/.zshrc && cp zshrc ~/.zshrc

chsh -s /bin/zsh


### deprecated ###
## install ncurses
#ncurses_path=https://ftp.gnu.org/gnu/ncurses/ncurses-6.1.tar.gz
#wget $ncurses_path 
#tar -zxvf ncurses-6.1.tar.gz
#cd ncurses-6.1
#export CXXFLAGS=' -fPIC'
#export CFLAGS=' -fPIC'
#./configure --prefix=$HOME/.local --enable-shared
#make
#make install
## Deduce environment information and build private terminfo tree
#cd progs
#./capconvert
#cd ..
#rm ncurses-6.1* -rf

## config path
#INSTALL_PATH='$HOME/.local'
#export PATH=$INSTALL_PATH/bin:$PATH
#export LD_LIBRARY_PATH=$INSTALL_PATH/lib:$LD_LIBRARY_PATH
#
#export LDFLAGS=-L$INSTALL_PATH/lib
#export C_INCLUDE_PATH=$C_INCLUDE_PATH:$INSTALL_PATH/include/ncurses
#export CPLUS_INCLUDE_PATH=$CPLUS_INCLUDE_PATH:$INSTALL_PATH/include/ncurses
#export CFLAGS=-I$INSTALL_PATH/include/ncurses
#export CPPFLAGS=-I$INSTALL_PATH/include/ncurses

## install zsh from src
#wget -O zsh.tar.gz https://sourceforge.net/projects/zsh/files/latest/download
#mkdir zsh && tar -xvzf zsh.tar.gz -C zsh --strip-components 1
#cd zsh
#autoheader
#autoconf
#date < stamp-h.in
#./configure --prefix=$HOME/.local --enable-shared \
#    --includedir=$INSTALL_PATH/include \
#    CFLAGS=-I$INSTALL_PATH/include/ncurses CXXFLAGS=-I$INSTALL_PATH/include/ncurses
#make
#make install
