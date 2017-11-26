#!/bin/bash
sudo apt-get install -y build-essential
sudo apt-get install -y cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get install -y python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev

if [ ! -d ~/src/opencv ];then
    mkdir ~/src/opencv
fi
cd ~/src/opencv

git clone https://github.com/Itseez/opencv.git
git clone https://github.com/Itseez/opencv_contrib.git

cd opencv
mkdir release
cd release
cmake -D WITH_IPP=OFF -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D OPENCV_EXTRA_MODULES_PATH=${HOME}/src/opencv/opencv_contrib/modules ..
make -j5
sudo make install

cd ~/
git clone https://github.com/duinodu/testopencvinstall.git
cd testopencvinstall
sudo chmod +x auto.sh
./auto.sh
cd build
./DisplayImage ../test.jpg
echo ""
echo "opencv install successfully"
echo ""
cd ~
rm -rf testopencvinstall
