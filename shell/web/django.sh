#!/bin/bash -e

py_ver=`python -c 'import sys; print(sys.version_info[:][0])'`
if [[ $py_ver == '2' ]]; then
    echo "current using python2, switch to python3 instead."
    cd ~
    virtualenv -p python3 py3
    source py3/bin/activate
else
    echo "current using python3"
fi

pip install django graphene_django

if [ ! -d ~/project/web ];then
    mkdir -p ~/project/web
fi

cd ~/project/web

django-admin.py startproject django_demo
cd django_demo
python manage.py migrate
./manage.py runserver
