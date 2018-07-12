#!/bin/bash -e

if [ ! -n "$1" ];then
    echo "Usage: createlib [lib name]"
    exit 1
fi

libname=$1

git clone https://github.com/duinodu/samplemod
mv samplemod $libname

cd $libname
rm .git -rf

mv sample $libname
sed -i -e "s/samplemod/${libname}/g" setup.py
sed -i -e "s/sample/${libname}/g" tests/context.py 
sed -i -e "s/sample/${libname}/g" tests/test_basic.py

git init
git add .
git commit -m 'init'
