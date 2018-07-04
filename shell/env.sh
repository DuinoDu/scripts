#!/bin/bash
PWD=`pwd`
#sudo apt-get update -y
#sudo apt-get install cmake python-dev python-pip -y
#
## git
#sudo git
#git config --global user.email "472365351duino@gmail.com"
#git config --global user.name "DuinoDu"
#
#
## vim
#sudo apt-get install vim-gtk -y
cd $PWD
cp envrc/vimrc ~/.vimrc
mkdir -p ~/.vim/bundle
cd ~/.vim/bundle
git clone https://github.com/gmarik/Vundle.vim.git
cd ~/.vim
git clone https://github.com/duinodu/UltiSnips
vim +PluginInstall +qall


## python-env
#cd ~
#sudo pip install --upgrade pip
#sudo pip install virtualenv
#virtualenv py2
#virtualenv -p python3 py3
#source ~/py2/bin/activate


## python lib
#sudo pip install numpy 
#pip install scipy matplotlib pandas jupyter
#pip install sklearn scikit-image opencv-python 

# DL 
# cuda9.0
# NVIDIA driver: http://www.nvidia.com/Download/index.aspx?lang=en-us
# cuda: https://developer.nvidia.com/cuda-downloads
# cudnn: https://developer.nvidia.com/rdp/cudnn-download
#pip install mxnet-cu90
#pip install http://download.pytorch.org/whl/cu90/torch-0.3.0.post4-cp27-cp27mu-linux_x86_64.whl
#pip install tensorflow-gpu
#pip install tensorboard-pytorch tensorflow-tensorboard
#pip install torchvision torchtext 


# SLAM

# tmux
#sudo apt-get install tmux zsh curl
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
chsh -s /bin/zsh



## pytorch from source
#cd ~
#mkdir src && cd src
#git clone --recursive https://github.com/pytorch/pytorch
#cd pytorch
#pip install -r requirements.txt
#python setup.py install
#echo "export PATH=~/project/scripts/python:\$PATH >> ~/.zshrc"
#echo "export PATH=~/project/scripts/shell:\$PATH >> ~/.zshrc"
