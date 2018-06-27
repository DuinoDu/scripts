#!/bin/sh -ex

if [ ! -d ~/project/web ];then
    mkdir -p ~/project/web
fi

cd ~/project/web

git clone https://github.com/creativetimofficial/material-kit-react
git clone https://github.com/creativetimofficial/material-dashboard-react/
