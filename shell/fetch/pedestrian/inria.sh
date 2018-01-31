#!/bin/bash

cd ~
if [ ! -d data/pedestrain/inria ];then
    mkdir -p data/pedestrain/inria
fi
cd data/pedestrain/inria

wget ftp://ftp.inrialpes.fr/pub/lear/douze/data/INRIAPerson.tar
tar -cxf INRIAPerson.tar
