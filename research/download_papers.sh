#!/usr/bin/env bash

arr=(
ICCV2015
ICCV2017
ECCV2018
CVPR2015
CVPR2016
CVPR2017
CVPR2018
CVPR2019
)
for item in ${arr[@]};do
    if [ ! -d $item ];then
        mkdir -p $item
    fi
    cd $item
    wget --recursive --level=1 --no-directories --no-host-directories --accept pdf http://openaccess.thecvf.com/${item}.py
    cd ..
done
