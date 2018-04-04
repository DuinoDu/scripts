#!/bin/bash

if [ ! -n "$1" ];then
    echo "voc_from_disk.sh [tar folder]"
    exit 1
fi

cd ~
if [ ! -d data/VOCdevkit ];then
    mkdir -p data/VOCdevkit
fi
cd data/VOCdevkit

tar -xvf $1/VOCtrainval_06-Nov-2007.tar -C ~/data
tar -xvf $1/VOCtrainval_11-May-2012.tar -C ~/data
tar -xvf $1/VOCtest_06-Nov-2007.tar -C ~/data
tar -xvf $1/VOC2012test.tar -C ~/data

unzip $1/SegmentationClassAug.zip -d ~/data/VOCdevkit/VOC2012
unzip $1/SegmentationClassGT_msracver.zip -d /tmp
cd ~/data/VOCdevkit/VOC2012
mv SegmentationClass SegmentationClass.origin
mv /tmp/SegmentationClassGT/SegmentationClass .
mv /tmp/SegmentationClassGT/train_seg.txt ImageSets/Main/
mv /tmp/SegmentationClassGT/val_seg.txt ImageSets/Main/

echo "VOC2007 and VOC2012 are saved in ~/data/VOCdevkit"
