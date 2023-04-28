#!/bin/bash
cd $1
mkdir routing
mkdir no-routing

for ((i=0; i<$2; i++))
do
    cd routing
    mkdir trace$((2**$i))

    cd ../no-routing
    mkdir trace$((2**$i))

    cd ..
done