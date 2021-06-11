#!/usr/bin/env bash

# wget vim-8.2.tar.bz2
# refer to https://www.vim.org/download.php

cd vim82

make clean
rm src/auto/config.cache

./configure –enable-multibyte \
    --enable-fontset \
    --enable-xim \
    --enable-luainterp=dynamic \
    --enable-python3interp=yes \
    --enable-rubyinterp=dynamic \
    --enable-cscope \
    --enable-sniff \
    --with-x \
    --with-compiledby=erocpil \
    --with-features=huge \
    --with-python3-command=/bin/python3.6 \
    --with-python-config-dir=$(python3.6-config --configdir)

    # --enable-perlinterp \

make -j12

cp src/vim bin/
