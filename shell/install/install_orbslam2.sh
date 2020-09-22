#!/bin/bash -ex

# OpenCV >= 2.4.6
sudo apt-get install libopencv-dev -y

# Boost
sudo apt-get install libboost-dev -y

# OpenGL
sudo apt-get install -y mesa-common-dev libgl1-mesa-dev libglu1-mesa-dev libglew-dev
sudo apt-get install -y freeglut3-dev freeglut3
sudo apt-get install -y build-essential gdb subversion
sudo apt-get install -y automake autoconf libtool
sudo apt-get install -y libgtk2.0-dev libxmu-dev libxxf86vm-dev
sudo apt-get install -y binutils-gold
sudo apt-get install -y build-essential

if [ ! -d ~/src/orbslam2 ];then
    mkdir -p  ~/src/orbslam2
fi

# Pangolin
cd ~/src/orbslam2
git clone https://github.com/stevenlovegrove/Pangolin.git
cd Pangolin
mkdir build && cd build && cmake .. && make -j5 && sudo make install

# Eigen3
cd ~/src/orbslam2
wget http://bitbucket.org/eigen/eigen/get/3.2.8.tar.gz
tar zxvf 3.2.8.tar.gz
cd eigen*
mkdir build && cd build && cmake .. && make && sudo make install

# BLAS and LAPACK
sudo apt-get install -y libblas-dev
sudo apt-get install -y liblapack-dev

# DBoW2
cd ~/src/orbslam2
git clone https://github.com/dorian3d/DBoW2.git
cd DBoW2
mkdir build && cd build && cmake .. && make && sudo make install

# g2o
cd ~/src/orbslam2
git clone https://github.com/RainerKuemmerle/g2o.git
cd g2o 
mkdir build && cd build && cmake .. && make && sudo make install

# orb-slam2
git clone https://github.com/raulmur/ORB_SLAM2.git ORB_SLAM2
cd ORB_SLAM2
chmod +x build.sh
./build.sh


# Download dataset
cd ~/src/orbslam2
wget http://vision.in.tum.de/rgbd/dataset/freiburg1/rgbd_dataset_freiburg1_xyz.tgz
tar -zxvf rgbd_dataset_freiburg1_xyz.tgz
rm -rf rgbd_dataset_freiburg1_xyz.tgz

# Run a demo
cd ~/src/orbslam2/ORB_SLAM2/Examples/Monocular
./mono_tum ../../Vocabulary/ORBvoc.txt TUM1.yaml ../../../rgbd_dataset_freiburg1_xyz
