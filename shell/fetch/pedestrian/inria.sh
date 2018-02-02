#!/bin/bash

cd ~
dir=data/pedestrian/INRIAPerson
if [ ! -d $dir ];then
    mkdir -p $dir
fi
cd $dir

wget ftp://ftp.inrialpes.fr/pub/lear/douze/data/INRIAPerson.tar
tar xvf INRIAPerson.tar
