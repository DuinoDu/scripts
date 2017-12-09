#!/bin/bash

if [ ! -n "$1" ];then
    echo "./6_fetch_cite_from_tex.sh [tex file]"
    exit 1
fi

if [ ! -d papers ];then
    mkdir papers
fi

result=`grep -P -o '\d{4}\.\d+' $1`
for r in ${result[*]}; do
    touch papers/$r.pdf
done
