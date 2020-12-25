#!/usr/bin/env bash

SIP_VERSION=4.19
QT_VERSION=5.7.1

echo "###############################################################"
echo "Start the installation of sip,which is an import tool to call "
echo "gcc compile source code of pyqt into binary code"
echo "###############################################################"
cd ~/Downloads
wget http://sourceforge.net/projects/pyqt/files/sip/sip-${SIP_VERSION}/sip-${SIP_VERSION}.tar.gz
tar -xzf sip-${SIP_VERSION}.tar.gz
cd sip-${SIP_VERSION}
python configure.py --platform linux-g++ && \
    make && \
    sudo make install

echo "###############################################################"
echo "Start the installation of pyqt "
echo "It will take some time because we need to compile the souece code"
echo "###############################################################"
wget http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-${QT_VERSION}/PyQt5_gpl-${QT_VERSION}.tar.gz
tar -xzf PyQt5_gpl-${QT_VERSION}.tar.gz
cd PyQt5_gpl-${QT_VERSION}
python configure.py && \
    make && \
    sudo make install

echo "###############################################################"
echo "All the installation has done! please check your installation"
echo "###############################################################"
