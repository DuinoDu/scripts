#!/bin/bash

root=~/project/objdect/0_fRCNN/pytorch-faster-rcnn
if [ ! -d $root ];then
    echo "Please git clone https://github.com/ruotianluo/pytorch-faster-rcnn"
    exit
fi
cd $root


####################
# build lib
####################
ARCH=sm_61
CUDA_ROOT=/usr/local/cuda
if [ ! -d $CUDA_ROOT ];then
    if [ ! -L $CUDA_ROOT ];then
        echo "Not found cuda."
        exit
    fi
fi
function nvcc_build() {
    $CUDA_ROOT/bin/nvcc -std=c++11 -c -o $1.o $1 -x cu -Xcompiler -fPIC -arch=$ARCH
}
cd lib/nms/src/cuda
nvcc_build nms_kernel.cu
cd ../..
python build.py
cd $root
cd lib/layer_utils/roi_pooling/src/cuda
nvcc_build roi_pooling_kernel.cu
cd ../..
python build.py
cd $root

####################
# build coco api
####################
if [ ! -d data ];then
    mkdir data
fi

cd data
if [ ! -d coco ];then
    git clone https://github.com/pdollar/coco.git
    cd coco/PythonAPI
    make
fi
cd $root

#####################
# create dataset link
#####################

VOCroot=~/data/VOCdevkit
if [ ! -d data/VOCdevkit2007 ];then
    ln -s $VOCroot data/VOCdevkit2007
fi
if [ ! -d data/VOCdevkit2012 ];then
    ln -s $VOCroot data/VOCdevkit2012
fi


######################
# fetch pretrain-model
######################
if [ ! -d data/imagenet_weights ];then
    mkdir data/imagenet_weights
fi
cd data/imagenet_weights
if [ ! -L vgg16.pth ];then
    vgg16=`ls ~/.torch/models/vgg16-*.pth`
    if [ "$vgg16" = "" ];then
        python -c "from torchvision import models; vgg16 = models.vgg16(pretrained=True)"
    fi
    ln -s ~/.torch/models/vgg16-* vgg16.pth
fi

if [ ! -L res101.pth ];then
    res101=`ls ~/.torch/models/resnet101-*.pth`
    if [ "$res101" = "" ];then
        python -c "from torchvision import models; net = models.resnet101(pretrained=True)"
    fi
    ln -s ~/.torch/models/resnet101-* res101.pth
fi
cd $root
