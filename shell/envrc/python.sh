#!/bin/bash

# env
cd ~
#sudo pip install --upgrade pip
#sudo pip install virtualenv
virtualenv -p python2 py2
virtualenv -p python3 py3
echo "source ~/py2/bin/activate" >> ~/.bashrc
source ~/py2/bin/activate

# python lib
sudo pip install numpy opencv-python

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


## pytorch from source
#cd ~
#mkdir src && cd src
#git clone --recursive https://github.com/pytorch/pytorch
#cd pytorch
#pip install -r requirements.txt
#python setup.py install
#echo "export PATH=~/project/scripts/python:\$PATH >> ~/.zshrc"
#echo "export PATH=~/project/scripts/shell:\$PATH >> ~/.zshrc"
