#!/bin/bash

if [ ! -d ~/opt ];then
    mkdir ~/opt
fi

cd ~/Downloads
wget https://dl.google.com/dl/android/studio/ide-zips/3.0.1.0/android-studio-ide-171.4443003-linux.zip
unzip android-studio*

mv android-studio ~/opt
