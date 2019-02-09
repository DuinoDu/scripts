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
tar -C $prefix -xzf $filename

export PATH=$PATH:$prefix/go/bin
echo "export PATH=\$PATH:$prefix/go/bin"
