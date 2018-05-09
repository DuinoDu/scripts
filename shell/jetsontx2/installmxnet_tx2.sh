#!/bin/sh -ex

if [ ! -n "$1" ];then
    echo "Stage 1"

    sudo apt-get update
    sudo apt-get -y install git build-essential libatlas-base-dev libopencv-dev graphviz python-pip
    sudo pip install pip --upgrade
    sudo pip install setuptools numpy --upgrade
    sudo pip install graphviz jupyter
    
    cd ~/src
    if [ ! -d incubator-mxnet ];then
        git clone --recursive https://github.com/apache/incubator-mxnet
    else
        cd incubator-mxnet
        git pull
        cd ..
    fi
    cd incubator-mxnet
    cp make/config.mk .
    echo "USE_CUDA=1" >> config.mk
    echo "USE_CUDA_PATH=/usr/local/cuda" >> config.mk
    echo "USE_CUDNN=1" >> config.mk
    
    echo "edit \${mxnet_root}/3rdparty/mshadow/make/mshadow.mk"
    echo "MSHADOW_CFLAGS += -DMSHADOW_USE_PASCAL=1"
    exit
fi

echo "Stage 2"

cd ~/src/incubator-mxnet
make -j $(nproc) USE_OPENCV=1 USE_BLAS=atlas USE_CUDA=1 USE_CUDA_PATH=/usr/local/cuda USE_CUDNN=1

cd python
pip install --upgrade pip
pip install -e .

cd ..
export MXNET_HOME=$(pwd)
echo "export PYTHONPATH=$MXNET_HOME/python:$PYTHONPATH" >> ~/.zshrc
source ~/.zshrc

python -c 'import mxnet as mx; print(mx.__file__)'
echo "Install mxnet from source successfully!"
