#!/usr/bin/env bash

TF_INC=$(python -c 'import tensorflow as tf; print(tf.sysconfig.get_include())')

# gcc 4 or using already-built binary,then set USE_CXX11_ABI=1
USE_CXX11_ABI=0

if [ ! -n "$1" ];then
    echo "Usage: maekOp xxx.cc"
    exit 1
fi

opName=$1
opName=${opName%.*}

echo ${opName}_gpu.cu.cc

ONLY_CPU=0
if [ ! -f ${opName}_gpu.cu.cc ];then
    ONLY_CPU=1
fi


if [[ "$ONLY_CPU" -eq 1 ]]; then
    # build only with cpu
    echo "Only CPU"
    g++ -std=c++11 -shared ${opName}.cc -o ${opName}.so -fPIC -I $TF_INC -O2

else
    # build with gpu
    echo "CPU & GPU"
    g++ -std=c++11 -shared ${opName}.cc -o ${opName}.so -fPIC -I $TF_INC -O2
    CUDA_PATH=/usr/local/cuda/
    if [ ! -d $CUDA_PATH ];then
        echo "Not found cuda"
        exit
    fi
    ${CUDA_PATH}/bin/nvcc -std=c++11 -c -o ${opName}.cu.o ${opName}_gpu.cu.cc \
    	-I $TF_INC -D GOOGLE_CUDA=1 -x cu -Xcompiler -fPIC -arch=sm_52
    
    g++ -std=c++11 -shared -D_GLIBCXX_USE_CXX11_ABI=$USE_CXX11_ABI -o ${opName}.so ${opName}.cc ${opName}.cu.o -I $TF_INC -fPIC -lcudart -L $CUDA_PATH/lib64
fi

if [ -f ${opName}.cu.o ];then
    rm ${opName}.cu.o
fi
