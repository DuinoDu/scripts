##!/bin/bash
# PWD=`pwd`
#sudo apt-get update -y
#sudo apt-get install cmake python-dev python-pip -y
#
## git
#sudo git
#git config --global user.email "472365351duino@gmail.com"
#git config --global user.name "DuinoDu"


## vim
#sudo apt-get install vim-gtk -y
#cd $PWD
#cp envrc/vimrc ~/.vimrc
#mkdir -p ~/.vim/bundle
#cd ~/.vim/bundle
#git clone https://github.com/gmarik/Vundle.vim.git
#cd ~/.vim
#git clone https://github.com/duinodu/UltiSnips
#vim -c 'PluginInstall' 


## python-env
#cd ~
#sudo pip install --upgrade pip
#sudo pip install virtualenv
#virtualenv py2
#virtualenv -p python3 py3
#source ~/py2/bin/activate
#
## pytorch
#cd ~
#mkdir src && cd src
#git clone --recursive https://github.com/pytorch/pytorch
#cd pytorch
#pip install numpy scipy matplotlib pandas
#pip install -r requirements.txt
#python setup.py install
#
## pip package
#pip install torchvision torchtext opencv-python jupyter
#pip install sklearn scikit-image
#pip install tensorflow tensorflow-tensorboard
#pip install tensorboard-pytorch
#pip install mxnet

# SLAM

# tmux
sudo apt-get install tmux
sudo apt-get install zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
chsh -s /bin/zsh
