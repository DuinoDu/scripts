#!/bin/bash -e

# https://golang.org/dl/

version=1.11.5
os=`uname | tr '[A-Z]' '[a-z]'`
filename=go${version}.${os}-amd64.tar.gz
target=https://dl.google.com/go/$filename

prefix=$HOME/opt
if [ ! -d $prefix ];then
    mkdir -p $prefix
fi

curl $target -fJO

filename=ggo1.11.5.linux-amd64.tar.gz
#hadoop fs -get hdfs://hobot-bigdata/user/min.du/go1.11.5.linux-amd64.tar.gz

tar -C $prefix -xzf $filename
rm $filename 

export PATH=$PATH:$prefix/go/bin
echo "export PATH=\$PATH:$prefix/go/bin"
