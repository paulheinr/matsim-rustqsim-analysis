#!/bin/bash
cd $1

for ((i=0; i<$2; i++))
do
    mkdir output-$((2**$i))
    cd output-$((2**$i))
    mkdir trace
    cd ..
done