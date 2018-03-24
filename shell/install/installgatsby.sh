#!/bin/bash

npm install --global gatsby-cli
if [ ! -d ~/project ];then
    mkdir ~/project
fi
cd ~/project

gatsby new gatsby-blog https://github.com/gatsbyjs/gatsby-starter-blog
cd gatsby-blog
gatsby develop
