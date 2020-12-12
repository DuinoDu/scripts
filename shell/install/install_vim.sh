#!/bin/bash
cd ~/
sudo apt-get -y update
sudo apt-get -y install vim-gtk git
mkdir -p ~/.vim/bundle
cd ~/.vim/bundle
git clone https://github.com/gmarik/Vundle.vim.git

cd ~/Downloads
wget http://prdownloads.sourceforge.net/ctags/ctags-5.8.tar.gz
tar -zxvf ctags-5.8.tar.gz
cd ctags-5.8
./configure
make
sudo make install
rm ctags-5.8.tar.gz ctags-5.8 -rf
touch ~/.vimrc
