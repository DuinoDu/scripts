#!/bin/bash

root=~/project/objdect/2_FPN/FPN
if [ ! -d $root ];then
    echo "Please git clone https://github.com/xmyqsh/FPN"
    exit
fi
cd $root

##########################
# check tensorflow version
##########################
#tf_version=`python -c "import tensorflow as tf; print(tf.__version__.replace('.', ''))"`
#if [ ! "$tf_version" -ge "120" ]; then
#    echo "tensorflow should >= v1.2.0"
#    read -p "if update tensorflow?[y/n]" update
#    if [ "$update" = "y" ]; then
#        pip install tensorflow_gpu>=1.2.0
#    else
#        exit
#    fi
#fi


if [ ! -d data ];then
    mkdir data
fi


#####################
# create dataset link
#####################
VOCroot=~/data/VOCdevkit
ln -s $VOCroot data/VOCdevkit2007

cd lib
make clean
make
cd ..


######################
# fetch pretrain-model
######################
if [ ! -d data/pretrain_model ];then
    mkdir data/pretrain_model
fi
echo "fetch Resnet50.npy from https://drive.google.com/file/d/0B_xFdh9onPagSWU1ZTAxUTZkZTQ/view, \
    and save it in data/pretrain_model."
