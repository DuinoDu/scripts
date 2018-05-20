#!/bin/bash 

if hash matlab 2>/dev/null;then
    echo "Find matlab : "`which matlab`
else
    echo 'matlab not found, please install matlab first.'
    exit
fi

if [ ! -d ~/project ];then
    mkdir ~/project
fi
cd ~/project

git clone https://github.com/votchallenge/vot-toolkit
cd vot-toolkit

echo "Add ~/project/vot-toolkit path to matlab default path list"
if [ -f /tmp/addpath_tmp.m ];then
    rm /tmp/addpath_tmp.m
fi
echo "addpath(genpath('$HOME/project/vot-toolkit'))" >> /tmp/addpath_tmp.m
echo "savepath" >> /tmp/addpath_tmp.m
echo "quit" >> /tmp/addpath_tmp.m
sudo matlab -nodisplay -nosplash -nodesktop -r "run /tmp/addpath_tmp.m"
rm /tmp/addpath_tmp.m

mkdir vot-workspace 
cd vot-workspace
matlab -nodisplay -nosplash -nodesktop

echo "1. execute workspace_create and choose experiment stack(vot2013)"
echo "2. execute run run_test.m to download sequences(data)"
