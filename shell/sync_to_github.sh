#!/bin/bash

set -e

for item in `ls .`;do
    if [ ! -d ${item} ];then
        continue
    fi
    echo $item
    
    if [[ "${exists[@]}" =~ $item  ]] ; then
        echo ${item} exists.
        continue
    # else
    #     echo ${item} not exists.
    fi

    gh repo create duinodu/${item}  --private -y
    cd ${item}
    git add . -A
    git commit -m 'update'
    git branch -M main
    git push -u origin main
    cd ..
done
