#!/bin/bash


if [ ! -d ~/data/posetrack ];then
    mkdir ~/data/posetrack
fi
cd ~/data/posetrack

if [ ! -d tar ];then
    mkdir tar
fi
cd tar

image0='https://datasets.d2.mpi-inf.mpg.de/posetrack/posetrack_data_images.tar.batch00'
image1='https://datasets.d2.mpi-inf.mpg.de/posetrack/posetrack_data_images.tar.batch01'
image2='https://datasets.d2.mpi-inf.mpg.de/posetrack/posetrack_data_images.tar.batch02'
image3='https://datasets.d2.mpi-inf.mpg.de/posetrack/posetrack_data_images.tar.batch03'
image4='https://datasets.d2.mpi-inf.mpg.de/posetrack/posetrack_data_images.tar.batch04'
image5='https://datasets.d2.mpi-inf.mpg.de/posetrack/posetrack_data_images.tar.batch05'
image6='https://datasets.d2.mpi-inf.mpg.de/posetrack/posetrack_data_images.tar.batch06'
image7='https://datasets.d2.mpi-inf.mpg.de/posetrack/posetrack_data_images.tar.batch07'
anno='https://datasets.d2.mpi-inf.mpg.de/posetrack/posetrack_v0.75_labels.tar'
test='https://posetrack.net/data/test.tar.gz'

wget $image0
wget $image1
wget $image2
wget $image3
wget $image4
wget $image5
wget $image6
wget $image7
wget $anno
wget $test

cd ..
cat tar/*.tar* | tar -xvf - -i
tar -xvf tar/posetrack_v0.75_labels.tar
tar -zxvf tar/test.tar.gz

git clone https://github.com/leonid-pishchulin/poseval 

echo "mpii is in ~/data/mpii"
