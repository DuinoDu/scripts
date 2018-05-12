#!/bin/bash -ex

# ubuntu 16.04
echo "Install libfreenect2 on ubuntu 16.04"

if [ ! -d ~/src ];then
    mkdir ~/src
fi
cd ~/src

git clone https://github.com/OpenKinect/libfreenect2.git
cd libfreenect2

sudo apt-get install build-essential cmake pkg-config
sudo apt-get install libusb-1.0-0-dev
sudo apt-get install libturbojpeg libjpeg-turbo8-dev
sudo apt-get install libglfw3-dev
sudo apt-get install libjpeg-dev #libva-dev 
sudo apt-get install libopenni2-dev

mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local/
make
sudo make install


# prepare for device
sudo cp ../platform/linux/udev/90-kinect2.rules /etc/udev/rules.d/

echo "plug kinect2"
exit

echo "increase USBFS buffer size"
sudo sh -c 'echo 128 > /sys/module/usbcore/parameters/usbfs_memory_mb'
./bin/Protonect

echo "If failed with [bulk transfer failed: LIBUSB_ERROR_IO Input/Output Error]"
echo "Refer to https://github.com/OpenKinect/libfreenect2/issues/807"

# run openni2 test
cd build
sudo apt-get install openni2-utils
sudo make install-openni2
LIBFREENECT2_PIPLINE=cuda
NiViewer2
