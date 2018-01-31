#!/bin/bash

cd ~
dir='data/pedestrain/kitti'
if [ ! -d $dir ];then
    mkdir -p $dir
fi
cd $dir

wget http://kitti.is.tue.mpg.de/kitti/data_object_image_2.zip
wget http://kitti.is.tue.mpg.de/kitti/data_object_label_2.zip

unzip data_object_image_2.zip
unzip data_object_label_2.zip
