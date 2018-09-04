#!/bin/bash
# File              : install_firefox.sh
# Author            : du min <min.du@hobot.cc>
# Date              : 26.07.2018
# Last Modified Date: 26.07.2018
# Last Modified By  : du min <min.du@hobot.cc>

if hash firefox 2>/dev/null;then
    echo "Find firefox : `which firefox`"
    read -p "Still install firefox? [y/n]" override
    if [[ $override = "n"  ]]; then
        exit
    fi
else
    echo 'firefox not found, install firefox'
fi

#firefox_root="https://ftp.mozilla.org/pub/firefox/nightly/2017/04/2017-04-18-07-47-00-mozilla-aurora"
#firefox_version="firefox-54.0a2.en-US.linux-x86_64.tar.bz2"

firefox_v=53.0
firefox_root="https://ftp.mozilla.org/pub/firefox/releases"
firefox_version="${firefox_v}/linux-x86_64/zh-CN/firefox-${firefox_v}.tar.bz2"

driver_root="https://github.com/mozilla/geckodriver/releases/download"
driver_version="v0.21.0/geckodriver-v0.21.0-linux64.tar.gz"

cd ~
if [ ! -d opt ];then
    mkdir opt
fi
cd opt

if [ -d firefox ];then
    read -p "Override existing firefox? [y/n]" override
    if [[ $override = "y"  ]]; then
        rm -rf firefox
    else
        exit
    fi
fi

wget $firefox_root/$firefox_version -O firefox.tar.bz2
tar xvf firefox.tar.bz2
rm firefox.tar.bz2

wget $driver_root/$driver_version -O firefox_driver.tar.gz
tar zxvf firefox_driver.tar.gz
rm firefox_driver.tar.gz

python_path=$(dirname $(which python))
mv geckodriver $python_path
if [ -l $python_path/firefox ];then
    rm $python_path/firefox
fi
ln -s $(pwd)/firefox/firefox $python_path/firefox

echo "Install firefox and selenium driver successfully"
