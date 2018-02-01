#!/bin/bash

cd ~
if [ ! -d data/pedestrian/inria ];then
    mkdir -p data/pedestrian/inria
fi
cd data/pedestrian/inria

wget ftp://ftp.inrialpes.fr/pub/lear/douze/data/INRIAPerson.tar
tar -cxf INRIAPerson.tar
