@echo off

curl https://nodejs.org/dist/v8.11.3/node-v8.11.3-x64.msi --output ~/node-v8.11.3-x64.msi
msiexec.exe ~/node-v8.11.3-x64.msi

echo "npm install -g windows-build-tools in powershell with admin mode"

gatsby new gatsby-blog https://github.com/gatsbyjs/gatsby-starter-blog
cd gatsby-blog
gatsby develop
