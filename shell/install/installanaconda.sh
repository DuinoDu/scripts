#!/bin/bash -ex


filename=Anaconda2-4.0.0-Linux-x86_64.sh
#filename=Anaconda3-5.2.0-Linux-x86_64.sh

cd ~/
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/$filename
chmod +x $filename
./$filename

export PATH="/home/users/min.du/anaconda2/bin:$PATH" 
conda update conda

echo "---"
echo "install caffe2"
echo ">>> conda install -c caffe2 caffe2-cuda9.0-cudnn7"
echo "or"
echo ">>> conda install -c caffe2 caffe2-cuda8.0-cudnn7"
echo "or in cpu mode"
echo ">>> conda install -c caffe2 caffe2"
