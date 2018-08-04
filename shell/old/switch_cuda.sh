#!/bin/bash

LINE_ID=98  # line id in .zshrc
function switch() {
    sed -i "${LINE_ID}c VERSION=$1" ~/.zshrc
    cd /usr/local
    if [ -L cuda ];then
        sudo rm cuda
    fi 
    sudo ln -s cuda-${1}.0 cuda
}

CURRENT=`ls -lh /usr/local/cuda | cut -d '-' -f 3`
if [[ $CURRENT =~ 9.* ]];then
    echo 'cuda-9.0 => cuda-8.0'
    switch 8
else
    echo 'cuda-8.0 => cuda-9.0'
    switch 9
fi

