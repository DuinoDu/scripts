#!/bin/sh

set -x
set -e

sudo apt-get update
sudo apt-get install -y build-essential git
sudo apt-get install -y libopenblas-dev liblapack-dev
sudo apt-get install -y libopencv-dev
sudo apt-get install libc6-dev-i386

cd ~/src
if [ ! -d incubator-mxnet ];then
    git clone --recursive https://github.com/apache/incubator-mxnet
else
    cd incubator-mxnet
    git pull
    cd ..
fi


# add ROI Align
git clone https://github.com/TuSimple/mx-maskrcnn
cd mx-maskrcnn/rcnn/CXX_OP/
cp roi_align.cc roi_align.cu roi_align-inl.h ~/src/incubator-mxnet/src/operator/
cp *v1* ~/src/incubator-mxnet/src/operator/contrib
cd ~/src && rm mx-maskrcnn -rf


cd incubator-mxnet
#make -j $(nproc) USE_OPENCV=1 USE_BLAS=openblas USE_CUDA=1 USE_CUDA_PATH=/usr/local/cuda USE_CUDNN=1
make -j $(nproc) USE_OPENCV=1 USE_BLAS=openblas USE_CUDA=0 USE_CUDNN=0

cd python
pip install --upgrade pip
pip install -e .

sudo apt-get install graphviz
pip install graphviz

python -c 'import mxnet as mx; print(mx.__file__)'
echo "Install mxnet from source successfully!"
