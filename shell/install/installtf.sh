#!/usr/bin/env bash

## Build bazel
echo "Build bazel"
BAZEL_NAME=bazel-0.4.4-dist.zip
BAZEL_URL=https://github.com/bazelbuild/bazel/releases/download/0.4.4/${BAZEL_NAME}
cd ~/src
if [ ! -d bazel ];then
    mkdir bazel
fi
cd bazel
wget $BAZEL_URL
unzip $BAZEL_NAME 
bash ./compile.sh
sudo ln -s `pwd`/output/bazel /usr/local/bin/bazel

## Build tensorflow
cd ~/src
if [ ! -d tensorflow ];then
    rm -rf tensorflow
fi
git clone https://github.com/tensorflow/tensorflow
cd tensorflow
echo "1. cd ~/scr/tensorflow; ./configure"

echo "After that ,build python pip package"

# no sse
echo "2. bazel build --config=opt //tensorflow/tools/pip_package:build_pip_package"
# if using sse
echo "2. bazel build -c opt --copt=-mavx --copt=-mavx2 --copt=-mfma --copt=-mfpmath=both --copt=-msse4.2 --config=cuda -k //tensorflow/tools/pip_package:build_pip_package"

echo "if use CUDA, bazel build --config=opt --config=cuda //tensorflow/tools/pip_package:build_pip_package" 

echo "3. bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg"

echo "4. sudo pip install /tmp/tensorflow_pkg/*.whl"
