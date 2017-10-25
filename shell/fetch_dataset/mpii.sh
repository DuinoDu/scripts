#!/bin/bash

images='http://datasets.d2.mpi-inf.mpg.de/andriluka14cvpr/mpii_human_pose_v1.tar.gz'
annos='http://datasets.d2.mpi-inf.mpg.de/andriluka14cvpr/mpii_human_pose_v1_u12_2.zip'

if [ ! -d ~/data/mpii ];then
    mkdir -p ~/data/mpii
fi
cd ~/data/mpii

wget $images
wget $annos

for i in `ls *.tar.gz`;do
    tar -zxvf $i
done

for i in `ls *.zip`;do
    unzip $i
done

cd /tmp
git clone https://github.com/anewell/pose-hg-train
cd pose-hg-train/data/mpii
mv annot ~/data/mpii/annot_h5
cd /tmp && rm pose-hg-train -r

echo "mpii is in ~/data/mpii"
