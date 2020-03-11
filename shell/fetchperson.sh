#!/usr/bin/env bash

if [ ! -d person ];then
    mkdir -p person
fi
cd person

_ssh=git@gitlab.hobot.cc:
_http=http://gitlab.hobot.cc/

git clone ${_ssh}ptd/experimental/alg/Popeye/awesome-tools/tools.hobot.git
git clone ${_ssh}ptd/experimental/alg/Popeye/awesome-tools/dataperson.git
git clone ${_ssh}ptd/experimental/alg/Popeye/awesome-tools/devperson.git
git clone ${_ssh}ptd/experimental/alg/Popeye/awesome-tools/person-workflow.git
git clone ${_ssh}ptd/experimental/alg/Popeye/awesome-tools/visperson.git
git clone ${_ssh}ptd/experimental/aidi/toolkits/wyy.git
git clone ${_ssh}ptd/experimental/aidi/toolkits/hobot-utils-plotlog.git
