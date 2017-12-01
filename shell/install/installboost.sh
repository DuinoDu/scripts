#!/bin/sh

cd ~/src
if [ ! -d boost ];then
    mkdir boost
fi
cd boost

wget -O boost_1_55_0.tar.gz http://sourceforge.net/projects/boost/files/boost/1.55.0/boost_1_55_0.tar.gz .
tar xzvf boost_1_55_0.tar.gz
cd boost_1_55_0/
