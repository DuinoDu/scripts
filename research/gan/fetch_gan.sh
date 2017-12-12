#!/bin/bash

if [ ! -d ~/project/gan ];then
    mkdir -p ~/project/gan
fi
cd ~/project/gan

srez="https://github.com/david-gpu/srez"
pr_sr="https://github.com/leehomyc/Photo-Realistic-Super-Resoluton"
bicycle_gan="https://github.com/junyanz/BicycleGAN"
pix2pixHD="https://github.com/NVIDIA/pix2pixHD"
prog_gans="https://github.com/ptrblck/prog_gans_pytorch_inference"

code=($srez $pr_sr $bicycle_gan $pix2pixHD $prog_gans)

function fetch() {
    codes=$1
    for code in ${codes[*]} ; do
        if [ -d $code ];then
            echo $code "exist"
        else
            git clone --recursive $code
        fi
    done
}
fetch "${code[*]}"
