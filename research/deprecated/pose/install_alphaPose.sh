#!/bin/bash -ex

function checkcmd() {
    if hash $1 2>/dev/null;then
        echo "Find $2 : "
    else
        echo "$2 not found, please install th first."
        exit
    fi
}

cd ~/project
git clone https://github.com/MVIG-SJTU/AlphaPose.git
cd AlphaPose/human-detection/lib/
make clean
make
cd newnms/
make
cd ../../../

# install torch
# install tensorflow >= 1.2
checkcmd th torch

chmod +x install.sh
./install.sh

chmod +x fetch_models.sh
./fetch_models.sh
