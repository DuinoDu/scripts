#!/bin/sh
sudo apt-get install -y libprotobuf-dev libleveldb-dev libsnappy-dev libhdf5-serial-dev protobuf-compiler
#sudo apt-get install -y libopencv-dev
sudo apt-get install -y --no-install-recommends libboost-all-dev
sudo apt-get install libatlas-base-dev
sudo apt-get install libgflags-dev libgoogle-glog-dev liblmdb-dev
sudo apt-get install gfortran

#cd ~/src
#git clone https://github.com/BVLC/caffe.git
#
#cd caffe
#cp Makefile.config.example Makefile.config
## Adjust Makefile.config 
## set CPU_ONLY
## set MATLAB_DIR
#make all
#make test
#make runtest
#
#cd caffe
#sudo pip install -r requirements.txt
#make pycaffe
