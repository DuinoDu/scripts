#!/bin/bash

data=http://cg.cs.tsinghua.edu.cn/traffic-sign/data_model_code/data.zip
code=http://cg.cs.tsinghua.edu.cn/traffic-sign/data_model_code/code.zip

#data1=http://cg.cs.tsinghua.edu.cn/traffic-sign/data_model_code/nosign_1.zip
#data2=http://cg.cs.tsinghua.edu.cn/traffic-sign/data_model_code/nosign_2.zip
#data3=http://cg.cs.tsinghua.edu.cn/traffic-sign/data_model_code/nosign_3.zip
#data4=http://cg.cs.tsinghua.edu.cn/traffic-sign/data_model_code/nosign_4.zip
#data5=http://cg.cs.tsinghua.edu.cn/traffic-sign/data_model_code/nosign_5.zip
#data6=http://cg.cs.tsinghua.edu.cn/traffic-sign/data_model_code/nosign_6.zip

if [ ! -d ~/data ];then
    mkdir ~/data
fi
cd ~/data

if [ ! -d TT100K ];then
    mkdir TT100K
fi
cd TT100K

wget $data
wget $code


#wget $data1
#wget $data2
#wget $data3
#wget $data4
#wget $data5
#wget $data6

echo "Tsinghua-Tencent100K are downloaded in ~/data/TT100K"
