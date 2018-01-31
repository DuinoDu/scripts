#!/bin/bash

cd ~/
if [ ! -d data/pedestrian/citypersons ];then
    mkdir -p  data/pedestrian/citypersons
fi
cd data/pedestrian/citypersons

wget https://bitbucket.org/shanshanzhang/citypersons/get/c13bbdfa9862.zip
unzip c13bbdfa9862.zip

echo "open"
echo "https://www.cityscapes-dataset.com/file-handling/?packageID=3"
echo "to download images"
