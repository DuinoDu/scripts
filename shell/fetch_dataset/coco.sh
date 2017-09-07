#!/bin/bash

2014train='http://msvocds.blob.core.windows.net/coco2014/train2014.zip'
2014val='http://msvocds.blob.core.windows.net/coco2014/val2014.zip'
2014test='http://msvocds.blob.core.windows.net/coco2014/test2014.zip'
2015test='http://msvocds.blob.core.windows.net/coco2015/test2015.zip'
2014trainval_object='http://msvocds.blob.core.windows.net/annotations-1-0-3/instances_train-val2014.zip'
2014trainval_key='http://msvocds.blob.core.windows.net/annotations-1-0-3/person_keypoints_trainval2014.zip'
2014trainval_caption='http://msvocds.blob.core.windows.net/annotations-1-0-3/captions_train-val2014.zip'
2014test_info='http://msvocds.blob.core.windows.net/annotations-1-0-4/image_info_test2014.zip'
2015test_info='http://msvocds.blob.core.windows.net/annotations-1-0-4/image_info_test2015.zip'

if [ ! -d ~/data/coco ];then
    mkdir -p ~/data/coco
fi
cd ~/data/coco

wget $2014train
wget $2014train
wget $2014val
wget $2014test
wget $2015test
wget $2014trainval_object
wget $2014trainval_key
wget $2014trainval_caption
wget $2014test_info
wget $2015test_info

for i in `ls *.zip`;do
    unzip $i
done

mkdir zip
mv *.zip zip/

echo "mscoco is in ~/data/coco"
