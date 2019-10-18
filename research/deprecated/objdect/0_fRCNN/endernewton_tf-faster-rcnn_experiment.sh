#!/bin/bash

root=~/project/objdect/0_fRCNN/tf-faster-rcnn

if [ ! -d $root ];then
    echo "Please git clone https://github.com/endernewton/tf-faster-rcnn"
    exit
fi
cd $root

GPUID=0
method="Faster RCNN(tf)"

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
