#!/bin/bash

if [ "$1" == "" ]; then
  echo "Usage: cp.sh <GeoTools Directory>"
  exit
fi

if [ ! -e "$1" ]; then
  echo "Error: No such directory $1"
  exit
fi

base=`cd $1; pwd`
cp=''
for x in `ls $base/*.jar`; do
  cp=$cp:$x
done
cp=${cp:1}
echo "CLASSPATH=\$CLASSPATH:$cp"
