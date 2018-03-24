#!/bin/bash

cls_attr_table=https://cvml.ist.ac.at/AwA2/AwA2-base.zip
image=https://cvml.ist.ac.at/AwA2/AwA2-data.zip

if [ ! -d ~/data/zsl/awa2 ];then
    mkdir -p ~/data/zsl/awa2
fi
cd ~/data/zsl/awa2


wget $cls_attr_table
echo "13GB"
wget $image
