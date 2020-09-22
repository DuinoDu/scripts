#!/bin/sh

set -x
set -e

cd ~/src
if [ ! -d incubator-mxnet ];then
    git clone --recursive https://github.com/apache/incubator-mxnet
else
    cd incubator-mxnet
    git pull
    cd ..
fi


cd incubator-mxnet
make -j $(nproc) USE_OPENCV=1 USE_BLAS=openblas USE_CUDA=1 USE_CUDA_PATH=/usr/local/cuda USE_CUDNN=1
#make -j $(nproc) USE_OPENCV=1 USE_BLAS=openblas USE_CUDA=0 USE_CUDNN=0

cd python
pip install --upgrade pip
pip install -e .

python -c 'import mxnet as mx; print(mx.__file__)'
echo "Install mxnet from source successfully!"
