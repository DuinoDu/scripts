#!/bin/bash

if [ ! -d ~/project ];then
    mkdir ~/project
fi
cd ~/project

git clone https://github.com/pjreddie/darknet
cd darknet
sed 's/GPU=0/GPU=1/g' Makefile
sed 's/CUDNN=0/CUDNN=1/g' Makefile
sed 's/OPENCV=0/OPENCV=1/g' Makefile
sed 's/OPENMP=0/OPENMP=1/g' Makefile
sed 's/DEBUG=1/DEBUG=0/g' Makefile

#echo "ARCH= -gencode arch=compute_53,code=[sm_53,sm_53]"

make -j ${nproc}

wget https://pjreddie.com/media/files/yolov3.weights --no-check-certificate
wget https://pjreddie.com/media/files/yolov3-tiny.weights --no-check-certificate

#./dartnet detector demo cfg/coco.cfg cfg/yolov3.cfg yolov3.weights
#./dartnet detector demo cfg/coco.cfg cfg/tiny-yolo.cfg tiny-yolo.weights
#./dartnet detector demo cfg/voc.cfg cfg/tiny-yolo-voc.cfg tiny-yolo-voc.weights
