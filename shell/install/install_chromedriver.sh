#!/bin/bash

version=2.42
os=mac64 # linux64, win32
wget https://chromedriver.storage.googleapis.com/$version/chromedriver_$os.zip 
unzip chromedriver_$os.zip
sudo mv chromedriver /usr/local/bin
rm chromedriver_$os.zip
