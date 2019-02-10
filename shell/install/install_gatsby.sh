#!/bin/bash

npm install --global gatsby-cli
if [ ! -d ~/project ];then
    mkdir ~/project
fi
cd ~/project

gatsby new gatsby-blog https://github.com/gatsbyjs/gatsby-starter-blog
cd gatsby-blog
gatsby develop

# if failed,
# cd gatsby-blog
# cnpm install
# gatsby build
# gatsby serve
