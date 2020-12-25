#!/usr/bin/env bash

_root=https://github.com/open-mmlab

arr=(
mmcv
mmdetection
mmdetection3d
mmsegmentation
mmclassification
mmaction2
mmpose
mmediting
mmskeleton
mmfashion
mmstyles
)

for item in ${arr[@]};do
    if [ -d $item ];then
        continue
    fi
    git clone ${_root}/${item}
done
