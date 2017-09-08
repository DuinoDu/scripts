#!/bin/bash

sudo apt-get update
sudo apt-get install cmake python-dev

# git
sudo git
git config --global user.email "472365351duino@gmail.com"
git config --global user.name "DuinoDu"

# tmux
sudo apt-get install tmux
sudo apt-get install zsh
sudo sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

# vim
sudo apt-get install vim-gtk
mkdir -p ~/.vim/bundle
cd ~/.vim/bundle
git clone https://github.com/gmarik/Vundle.vim.git
echo "copy .vimrc from http://git.oschina.net/duino/codes/7pbqlme9ci218o4hrdztj14/raw?blob_name=vimrc"
vim -c 'PluginInstall' 

# python-env
cd ~
virtualenv py2
virtualenv -p python3 py3
source py2/bin/activate

# pytorch
cd ~
mkdir src && cd src
git clone --recursive https://github.com/pytorch/pytorch && cd src
pip install numpy scipy matplotlib pandas
pip install -r requirements.txt
python setup.py install

# pip package
pip install torchvision torchtext vidom opencv-python jupyter
pip install sklearn scikit-image

# download dataset
