#!/bin/bash

lsp1='http://sam.johnson.io/research/lsp_dataset_original.zip'
lsp2='http://sam.johnson.io/research/lspet_dataset.zip'

if [ ! -d ~/data/lsp/zip ];then
    mkdir -p ~/data/lsp/zip
fi

cd ~/data/lsp

if [ ! -d lsp ];then
    mkdir lsp
fi

if [ ! -d lspet ];then
    mkdir lspet
fi

cd zip

wget $lsp1
wget $lsp2

cd ../lsp
unzip ../zip/lsp_dataset_original.zip

cd ../lspet
unzip ../zip/lspet_dataset.zip

echo "LSP is in ~/data/lsp"
