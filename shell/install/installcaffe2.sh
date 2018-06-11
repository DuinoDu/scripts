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


# Clone Caffe2's source code from our Github repository
git clone --recursive https://github.com/pytorch/pytorch.git && cd pytorch
git submodule update --init

# Create a directory to put Caffe2's build files in
mkdir build && cd build

# Configure Caffe2's build
# This looks for packages on your machine and figures out which functionality
# to include in the Caffe2 installation. The output of this command is very
# useful in debugging.
cmake ..

# Compile, link, and install Caffe2
sudo make install

# Test
cd ~ && python -c 'from caffe2.python import core' 2>/dev/null && echo "Success" || echo "Failure"
