#!/bin/bash

npm install --global gatsby-cli
if [ ! -d ~/project ];then
    mkdir ~/project
fi

gatsby new gatsby-blog https://github.com/gatsbyjs/gatsby-starter-blog
cd ~/project/gatsby-blog
gatsby develop
