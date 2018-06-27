#!/bin/bash -ex

if [ ! -d ~/project/web ];then
    mkdir -p ~/project/web
fi

cd ~/project/web

codes=(material-kit-react material-dashboard-react light-bootstrap-dashboard-react now-ui-dashboard-react)

for item in ${codes[@]};do
    git clone https://github.com/creativetimofficial/${item}
done
