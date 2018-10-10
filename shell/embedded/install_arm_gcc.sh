#!/bin/bash -e

if [ Darwin = 'Darwin' ]; then
    brew tap PX4/homebrew-px4
    brew update
    brew install gcc-arm-none-eabi 
else
    echo "only support darwin"
fi
