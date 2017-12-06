#!/bin/bash

root=~/project/objdect/3_maskRCNN/FastMaskRCNN
if [ ! -d $root ];then
    echo "Please git clone https://github.com/CharlesShang/FastMaskRCNN"
    exit
fi
cd $root

# build coco tools
cd libs/datasets/pycocotools
make
cd $root

# create dataset link
if [ ! -d data ];then
    mkdir data
fi
cd data
ln -s ~/data/coco coco
cd $root
python download_and_convert_data.py

# fetch pretrained model
if [ ! -d data/pretrained_models ];then
    mkdir -p data/pretrained_models
fi
cd data/pretrained_models
wget http://download.tensorflow.org/models/resnet_v1_50_2016_08_28.tar.gz
tar -zxvf resnet_v1_50_2016_08_28.tar.gz
cd $root

# build lib
cd libs
make
cd $root
