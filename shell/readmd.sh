#!/usr/bin/env bash

if [ ! -n "$1" ];then
    echo "readmd xx.md"
    exit 1
fi

markdown_py $1 > /tmp/duino.html && firefox /tmp/duino.html && rm /tmp/duino.html
