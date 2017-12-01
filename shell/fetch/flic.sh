#!/bin/bash

if [ ! -d ~/data/humanpose/flic ];then
    mkdir ~/data/humanpose/flic
fi
cd ~/data/humanpose/flic

wget http://vision.grasp.upenn.edu/video/FLIC-full.zip
unzip FLIC-full.zip
rm -rf FLIC-full.zip
cd FLIC-full
wget http://cims.nyu.edu/~tompson/data/tr_plus_indices.mat

echo "LSP is in ~/data/humanpose/flic"
