#!/bin/sh

sudo apt-get install build-essential  
  
sudo add-apt-repository ppa:ubuntu-toolchain-r/test  
sudo apt-get update  
sudo apt-get install gcc-4.9 g++-4.9 cpp-4.9 gcc-4.9-locales g++-4.9-multilib libstdc++6-4.9-dbg gcc-4.9-multilib libgcc1-dbg libgomp1-dbg libitm1-dbg libatomic1-dbg libasan1-dbg liblsan0-dbg libtsan0-dbg libubsan0-dbg libcilkrts5-dbg libquadmath0-dbg lib32stdc++6-4.9-dbg libx32stdc++6-4.9-dbg  
sudo apt-get install g++ 
