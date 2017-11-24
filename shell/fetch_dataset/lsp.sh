#!/bin/bash

lsp1='http://192.168.73.132/sam.johnson.io/research/lsp_dataset_original.zip'
lsp2='http://192.168.73.130/sam.johnson.io/research/lspet_dataset.zip'

if [ ! -d ~/data/lsp ];then
    mkdir -p ~/data/lsp
fi
cd ~/data/lsp

wget $lsp1
wget $lsp2

for i in `ls *.zip`;do
    unzip $i
done

echo "LSP is in ~/data/lsp"
