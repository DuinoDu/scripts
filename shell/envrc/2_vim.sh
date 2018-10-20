#!/bin/bash

#sudo apt-get install vim-gtk -y
cp vimrc ~/.vimrc
mkdir -p ~/.vim/bundle
cd ~/.vim/bundle
git clone https://github.com/gmarik/Vundle.vim.git
cd ~/.vim
git clone https://github.com/duinodu/UltiSnips
vim +PluginInstall +qall
