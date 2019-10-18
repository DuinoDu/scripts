#!/bin/bash -ex

if [ ! -d ~/project/vot-toolkit/kcf-workspace ];then
    echo "Create vot-toolkit and kcf-workspace first"
    exit
fi
cd ~/project/vot-toolkit/kcf-workspace

git clone https://github.com/joaofaro/KCFcpp

echo "KCFcpp requires opencv3"
cd KCFcpp
mkdir build 
cd build
cmake ..
make
