#!/bin/bash

root=~/project/objdect/0_fRCNN/tf-faster-rcnn
if [ ! -d $root ];then
    echo "Please git clone https://github.com/endernewton/tf-faster-rcnn"
    exit
fi
cd $root

##########################
# check tensorflow version
##########################
tf_version=`python -c "import tensorflow as tf; print(tf.__version__.replace('.', ''))"`
if [ ! "$tf_version" -ge "120" ]; then
    echo "tensorflow should >= v1.2.0"
    read -p "if update tensorflow?[y/n]" update
    if [ "$update" = "y" ]; then
        pip install tensorflow_gpu>=1.2.0
    else
        exit
    fi
fi


#####################
# create dataset link
#####################
VOCroot=~/data/VOCdevkit
ln -s $VOCroot data/VOCdevkit2007


######################
# fetch pretrain-model
######################

if [ ! -d data/imagenet_weights ];then
    mkdir data/imagenet_weights
fi

cd data/imagenet_weights
wget -v http://download.tensorflow.org/models/vgg_16_2016_08_28.tar.gz
tar -xzvf vgg_16_2016_08_28.tar.gz
mv vgg_16.ckpt vgg16.ckpt
cd ../..

cd data/imagenet_weights
wget -v http://download.tensorflow.org/models/resnet_v1_101_2016_08_28.tar.gz
tar -xzvf resnet_v1_101_2016_08_28.tar.gz
mv resnet_v1_101.ckpt res101.ckpt
cd ../..
