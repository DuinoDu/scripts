#!/bin/bash

root=~/project/objdect/0_fRCNN/pytorch-faster-rcnn

if [ ! -d $root ];then
    echo "Please git clone https://github.com/ruotianluo/pytorch-faster-rcnn"
    exit
fi
cd $root

GPUID=1
method="Faster RCNN(pytorch)"

data=pascal_voc_0712
backbone=vgg16
./experiments/scripts/train_faster_rcnn.sh $GPUID $data $backbone 
log_file=`ls -Art experiments/logs | tail -n 1`
./write2tex.sh $log_file scripts_root/result.tex $method $data $backbone
backbone=res101
./experiments/scripts/train_faster_rcnn.sh $GPUID $data $backbone 
log_file=`ls -Art experiments/logs | tail -n 1`
./write2tex.sh $log_file scripts_root/result.tex $method $data $backbone

#data=pascal_voc
#backbone=vgg16
#./experiments/scripts/train_faster_rcnn.sh $GPUID $data $backbone 
#log_file=`ls -Art experiments/logs | tail -n 1`
#scripts_root/write2tex.sh $log_file scripts_root/result.tex $method $data $backbone
#backbone=res101
#./experiments/scripts/train_faster_rcnn.sh $GPUID $data $backbone 
#log_file=`ls -Art experiments/logs | tail -n 1`
#scripts_root/write2tex.sh $log_file scripts_root/result.tex $method $data $backbone
