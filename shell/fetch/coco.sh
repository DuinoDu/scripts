#!/bin/bash

coco_2014train="http://msvocds.blob.core.windows.net/coco2014/train2014.zip"
coco_2014val="http://msvocds.blob.core.windows.net/coco2014/val2014.zip"
coco_2014test="http://msvocds.blob.core.windows.net/coco2014/test2014.zip"
coco_2015test="http://msvocds.blob.core.windows.net/coco2015/test2015.zip"
coco_2014trainval_object="http://msvocds.blob.core.windows.net/annotations-1-0-3/instances_train-val2014.zip"
coco_2014trainval_key="http://msvocds.blob.core.windows.net/annotations-1-0-3/person_keypoints_trainval2014.zip"
coco_2014trainval_caption="http://msvocds.blob.core.windows.net/annotations-1-0-3/captions_train-val2014.zip"
coco_2014test_info="http://msvocds.blob.core.windows.net/annotations-1-0-4/image_info_test2014.zip"
coco_2015test_info="http://msvocds.blob.core.windows.net/annotations-1-0-4/image_info_test2015.zip"

coco_2017train="http://images.cocodataset.org/zips/train2017.zip"
coco_2017val="http://images.cocodataset.org/zips/val2017.zip"
coco_2017anno="http://images.cocodataset.org/annotations/annotations_trainval2017.zip"

data_root=~/data/public/coco
if [ ! -d $data_root ];then
    mkdir -p $data_root
fi
cd $data_root

#wget $coco_2014train
#wget $coco_2014train
#wget $coco_2014val
#wget $coco_2014test
#wget $coco_2015test
#wget $coco_2014trainval_object
#wget $coco_2014trainval_key
#wget $coco_2014trainval_caption
#wget $coco_2014test_info
#wget $coco_2015test_info

wget $coco_2017train
wget $coco_2017val
wget $coco_2017anno

for i in `ls *.zip`;do
    unzip $i
done

mkdir zip
mv *.zip zip/

echo "mscoco is in $data_root"
