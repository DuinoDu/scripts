#!/bin/bash -ex


filename=Anaconda2-4.0.0-Linux-x86_64.sh
#filename=Anaconda3-5.2.0-Linux-x86_64.sh

cd ~/
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/$filename
chmod +x $filename
./$filename
