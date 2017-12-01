#!/bin/sh
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt-get update
sudo apt-get install -y nvidia-370
sudo apt-get install -y mesa-common-dev
sudo apt-get install -y freeglut3-dev
sudo reboot
