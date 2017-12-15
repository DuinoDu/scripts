#!/bin/bash

if [ ! -n "$1" ];then
    echo "./gen_test.sh [input python file]"
    exit 1
fi

if [ ! -d test ];then
    mkdir test
fi

filename="test/test_${1}"
if [ -f $filename ];then
    echo "$filename exist."
    exit 1
fi

touch $filename

# add import libs
OLDIFS=$IFS
IFS="
"
import_items=($(grep 'import' $1))
for each in ${import_items[*]} ; do
    echo $each >> $filename 
done
IFS=$OLDIFS 

echo "import sys, os" >> $filename
echo "sys.path.append(os.path.join(os.path.dirname(__file__), '..'))" >> $filename

echo "from ${1%.py} import *" >> $filename
echo "" >> $filename

# add test_class
a=($(grep 'class ' $1 | cut -d ' ' -f 2 | cut -d '(' -f 1))
for each in ${a[*]} ; do
    echo "def test_${each}():" >> $filename 
    echo '    pass' >> $filename
    echo "" >> $filename
done

echo "" >> $filename
echo 'if __name__ == "__main__":' >> $filename
for each in ${a[*]} ; do
    echo "    test_${each}()" >> $filename   
done
