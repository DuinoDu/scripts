#!/bin/bash -ex

cd ~/project
git clone https://github.com/facebookresearch/Detectron
cd Detectron
pip install -r requirements.txt
make
python tests/test_spatial_narrow_as_op.py
