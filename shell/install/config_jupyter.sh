#!/bin/bash

jupyter notebook --generate-config

PORT=8181
passwd=`python -c "from notebook.auth import passwd; print(passwd(''))"`
echo "c.NotebookApp.ip='*'" >> ~/.jupyter/jupyter_notebook_config.py
echo "c.NotebookApp.password=u'"${passwd}"'" >> ~/.jupyter/jupyter_notebook_config.py
echo "c.NotebookApp.open_browser = False" >> ~/.jupyter/jupyter_notebook_config.py
echo "c.NotebookApp.port="${PORT} >> ~/.jupyter/jupyter_notebook_config.py

ip=`ifconfig | grep 'inet addr' | cut -f2 -d: | cut -d " " -f1`
for e in $ip;do
    echo "http://"${e}":"$PORT
done

echo "Done. Start jupyter and use it remotely."
