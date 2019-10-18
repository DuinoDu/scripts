#!/usr/bin/env bash

py_ver=`python -c 'import sys; print(sys.version_info[:][0])'`
if [[ $py_ver == '3' ]]; then
    echo "Please using python3"
    exit    
fi

pip install torch torchvision
pip install --verbose --no-cache-dir torch-scatter
pip install --verbose --no-cache-dir torch-sparse
pip install --verbose --no-cache-dir torch-cluster
pip install --verbose --no-cache-dir torch-spline-conv
pip install torch-geometric
