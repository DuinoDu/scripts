#!/bin/sh

iccv2015='http://www.pamitc.org/iccv15/files/iccv2015AuthorKit.zip'
wget $iccv2015
unzip iccv2015AuthorKit.zip
mv iccv2015AuthorKit/latex .
rm iccv2015AuthorKit* -rf
