#!/bin/bash

root=~/project/objdect/3_maskRCNN/FastMaskRCNN
if [ ! -d $root ];then
    echo "Please git clone https://github.com/CharlesShang/FastMaskRCNN"
    exit
fi
cd $root


function create_env_install_tf() {
    cd ~/
    if [ -d env_tf1_1 ];then
        echo "env_tf already exist."
        exit
    fi
    virtualenv env_tf1_1
    source env_tf1_1/bin/activate
    pip install tensorflow_gpu==1.1.0
    pip install scikit-image opencv-python
}


# check tensorflow version
tf_version=`python -c "import tensorflow as tf; print(tf.__version__.replace('.', ''))"`
if [ ! "$tf_version" -e "110" ]; then
    echo "tensorflow should == 1.1.0"
    read -p "if update tensorflow(it will create new virtualenv)?[y/n]" update
    if [ "$update" = "y" ]; then
        create_env_install_tf
    else
        exit
    fi
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
