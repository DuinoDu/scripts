#!/bin/bash

if [ ! -d ~/project ];then
    mkdir ~/project
fi
cd ~/project

if [ ! -n "$1" ];then
    git clone https://github.com/pjreddie/darknet
    cd darknet
    
    echo "edit Makefile"
    echo "GPU=1"
    echo "CUDNN=1"
    echo "OPENCV=1"
    echo "OPENMP=1"
    echo "DEBUG=0"
    echo "ARCH= -gencode arch=compute_53,code=[sm_53,sm_53]"
    exit 1
fi

cd darknet
make -j ${nproc}

wget https://pjreddie.com/media/files/yolov3.weights --no-check-certificate
wget https://pjreddie.com/media/files/yolov3-tiny.weights --no-check-certificate
wget https://pjreddie.com/media/files/yolov3-voc.weights --no-check-certificate

#./dartnet detector demo cfg/coco.cfg cfg/yolov3.cfg yolov3.weights
#./dartnet detector demo cfg/coco.cfg cfg/tiny-yolo.cfg tiny-yolo.weights
#./dartnet detector demo cfg/voc.cfg cfg/tiny-yolo-voc.cfg tiny-yolo-voc.weights
