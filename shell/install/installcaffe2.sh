#!/bin/sh

sudo apt-get update
sudo apt-get install -y --no-install-recommends \
      build-essential \
      cmake \
      git \
      libgoogle-glog-dev \
      libprotobuf-dev \
      protobuf-compiler \
      python-dev \
      python-pip                          
sudo pip install numpy protobuf

# 14.04
#sudo apt-get install -y --no-install-recommends libgflags2
# 16.04
sudo apt-get install -y --no-install-recommends libgflags-dev

sudo apt-get install -y --no-install-recommends \
      libgtest-dev \
      libiomp-dev \
      libleveldb-dev \
      liblmdb-dev \
      libopencv-dev \
      libopenmpi-dev \
      libsnappy-dev \
      openmpi-bin \
      openmpi-doc \
      python-pydot
sudo pip install \
      flask \
      graphviz \
      hypothesis \
      jupyter \
      matplotlib \
      pydot python-nvd3 \
      pyyaml \
      requests \
      scikit-image \
      scipy \
      setuptools \
      tornado

if [ ! -d ~/src ];then
    mkdir ~/src
fi
cd ~/src
git clone --recursive https://github.com/caffe2/caffe2.git && cd caffe2
make && cd build && sudo make install
python -c 'from caffe2.python import core' 2>/dev/null && echo "Success" || echo "Failure"
