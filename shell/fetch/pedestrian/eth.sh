#!/bin/bash

cd ~
dir='data/pedestrian/eth'
if [ ! -d $dir ];then
    mkdir -p $dir
fi
cd $dir

wget https://data.vision.ee.ethz.ch/cvl/aess/dataset/eth01.idl.gz 
wget https://data.vision.ee.ethz.ch/cvl/aess/dataset/eth02.idl.gz 
wget https://data.vision.ee.ethz.ch/cvl/aess/dataset/eth03.idl.gz 

# Setup1
wget https://data.vision.ee.ethz.ch/cvl/aess/cvpr2008/seq03-img-left.tar.gz
wget https://data.vision.ee.ethz.ch/cvl/aess/cvpr2008/seq03-img-right.tar.gz 
wget https://data.vision.ee.ethz.ch/cvl/aess/dataset/jelmoli-annot.idl
wget https://data.vision.ee.ethz.ch/cvl/aess/dataset/eth02.idl.gz

wget https://data.vision.ee.ethz.ch/cvl/aess/cvpr2008/seq04-img-left.tar.gz
wget https://data.vision.ee.ethz.ch/cvl/aess/cvpr2008/seq04-img-left1.tar.gz
wget https://data.vision.ee.ethz.ch/cvl/aess/cvpr2008/seq04-img-right.tar.gz
wget https://data.vision.ee.ethz.ch/cvl/aess/cvpr2008/seq04-img-right1.tar.gz
#wget https://data.vision.ee.ethz.ch/cvl/aess/dataset/jelmoli-annot.idl
#wget https://data.vision.ee.ethz.ch/cvl/aess/dataset/eth02.idl.gz

wget https://data.vision.ee.ethz.ch/cvl/aess/dataset/sunny_day-img-left.tar.gz
wget https://data.vision.ee.ethz.ch/cvl/aess/dataset/sunny_day-img-right.tar.gz
wget https://data.vision.ee.ethz.ch/cvl/aess/dataset/sunny_day-annot.idl

# Setup2
wget https://data.vision.ee.ethz.ch/cvl/aess/cvpr2008/seq02-img-left.tar.gz
wget https://data.vision.ee.ethz.ch/cvl/aess/cvpr2008/seq02-img-right.tar.gz
wget https://data.vision.ee.ethz.ch/cvl/aess/dataset/linthescher-annot.idl

wget https://data.vision.ee.ethz.ch/cvl/aess/cvpr2008/seq01-img-left.tar.gz
wget https://data.vision.ee.ethz.ch/cvl/aess/cvpr2008/seq01-img-right.tar.gz
#wget https://data.vision.ee.ethz.ch/cvl/aess/dataset/linthescher-annot.idl

wget https://data.vision.ee.ethz.ch/cvl/aess/cvpr2008/seq05-img-left.tar.gz
wget https://data.vision.ee.ethz.ch/cvl/aess/cvpr2008/seq05-img-right.tar.gz

# Setup3
wget https://data.vision.ee.ethz.ch/cvl/aess/dataset/lp-left.tar.gz
wget https://data.vision.ee.ethz.ch/cvl/aess/dataset/lp-right.tar.gz
wget https://data.vision.ee.ethz.ch/cvl/aess/dataset/lp-annot.idl
