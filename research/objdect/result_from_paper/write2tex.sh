#!/bin/bash

if [ ! -n "$1" ];then
    echo "./write2tex [log file] [tex file] [method] [dataset] [backbone]"
    exit 1
fi
if [ ! -n "$2" ];then
    echo "./write2tex [log file] [tex file]"
    exit 1
fi
if [ ! -n "$3" ];then
    echo "./write2tex [log file] [tex file] [method] [dataset] [backbone]"
    exit 1
fi
if [ ! -n "$4" ];then
    echo "./write2tex [log file] [tex file] [method] [dataset] [backbone]"
    exit 1
fi
if [ ! -n "$5" ];then
    echo "./write2tex [log file] [tex file] [method] [dataset] [backbone]"
    exit 1
fi

aps=`cat $1 | grep ^0`
texfile=$2
method=$3  #FasterRCNN
data=$4 #voc0712
backbone=$5 #vgg16

python -c "
import sys; 
texfile = sys.argv[2]
method = sys.argv[3]
data = sys.argv[4]
backbone = sys.argv[5]
mAP = sys.argv[1].split('\n')[-1]

aps = ''
for l in sys.argv[1].split('\n')[:-1]:
    aps += ' & ' + l

print(method, data, backbone, mAP, aps)

template = open(texfile, 'r').readlines()
new_t = []
for line in template:
    if line.startswith('%'):
        new_line = line.replace('method', method) \
                       .replace('data', data) \
                       .replace('backbone', backbone) \
                       .replace('mAP', mAP) \
                       .replace('aps', aps)[1:]
        new_t.append(new_line)
    new_t.append(line)
with open(texfile, 'w') as fid:
    for line in new_t:
        fid.write(line)
" "$aps" "$texfile" "$method" "$data" "$backbone"
