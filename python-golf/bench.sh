#!/usr/bin/env bash

sizes=(2 4 8 16 25 50 100 200 250 500 1000 2000 2500 5000 10000 15000)

for size in ${sizes[@]}; do 
  echo $size
  time python -m golf $size --silent >> time.log
done
