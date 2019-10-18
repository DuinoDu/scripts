#!/bin/bash

if [ ! -d ~/project/objdect ];then
    mkdir -p ~/project/objdect
fi
cd ~/project/objdect

folders=('0_fRCNN' '1_RFCN' '2_FPN' '3_maskRCNN' 'a_SSD' 'b_DSOD' 'c_RetinaNet')

fRCNN_pytorch1="https://github.com/ruotianluo/faster_rcnn_pytorch"
fRCNN_tf1="https://github.com/endernewton/tf-faster-rcnn"
fRCNN_mx=""

RFCN_pytorch1="https://github.com/PureDiors/pytorch_RFCN"
RFCN_deformable_mx="https://github.com/msracver/Deformable-ConvNets"

FPN_tf="https://github.com/xmyqsh/FPN"

maskRCNN_pytorch="https://github.com/felixgwu/mask_rcnn_pytorch"
maskRCNN_mx="https://github.com/TuSimple/mx-maskrcnn"
maskRCNN_tf1="https://github.com/CharlesShang/FastMaskRCNN"
maskRCNN_tf2="https://github.com/matterport/Mask_RCNN"

SSD_caffe="https://github.com/weiliu89/caffe.git"
SSD_pytorch="https//github.com/duinodu/ssd.startup"

DSOD_caffe="https://github.com/szq0214/DSOD"

RetinaNet_pytorch="https://github.com/c0nn3r/RetinaNet"

function fetch() {
    if [ ! -d $1 ];then
        mkdir $1
    fi
    cd $1 
    codes=$2
    for code in ${codes[*]} ; do
        if [[ "$code" = "" ]]; then
            echo "ignore $code"
        else
            git clone --recursive $code
        fi
    done
    cd ..
}


code=($fRCNN_pytorch1 $fRCNN_tf1  $fRCNN_mx)
fetch ${folders[0]} "${code[*]}"

code=($RFCN_pytorch1 $RFCN_deformable_mx)
fetch ${folders[1]} "${code[*]}"

code=($FPN_tf)
fetch ${folders[2]} "${code[*]}"

code=($maskRCNN_pytorch $maskRCNN_tf1 $maskRCNN_tf2 $maskRCNN_mx)
fetch ${folders[3]} "${code[*]}"

code=($SSD_caffe $SSD_pytorch)
fetch ${folders[4]} "${code[*]}"

code=($DSOD_caffe)
fetch ${folders[5]} "${code[*]}"

code=($RetinaNet_pytorch)
fetch ${folders[6]} "${code[*]}"

cd a_SSD/caffe
git checkout origin/ssd
