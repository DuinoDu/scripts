#!/bin/bash


if [ ! -d ~/data/zsl/cub ];then
    mkdir -p ~/data/zsl/cub
fi
cd ~/data/zsl/cub

data=http://www.vision.caltech.edu/visipedia-data/CUB-200-2011/CUB_200_2011.tgz
seg=http://www.vision.caltech.edu/visipedia-data/CUB-200-2011/segmentations.tgz

echo "1.1GB"
wget $data
wget $seg
