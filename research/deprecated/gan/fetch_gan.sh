#!/bin/bash

if [ ! -d ~/project/gan ];then
    mkdir -p ~/project/gan
fi
cd ~/project/gan

srez="https://github.com/david-gpu/srez"
pr_sr="https://github.com/leehomyc/Photo-Realistic-Super-Resoluton"
BicycleGAN="https://github.com/junyanz/BicycleGAN"
pix2pixHD="https://github.com/NVIDIA/pix2pixHD"
prog_gans_pytorch_inference="https://github.com/ptrblck/prog_gans_pytorch_inference"
progressive_growing_of_gans="https://github.com/tkarras/progressive_growing_of_gans"

code=($srez \
    $pr_sr \
    $BicycleGAN \
    $pix2pixHD \
    $prog_gans_pytorch_inference \
    $progressive_growing_of_gans)

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
