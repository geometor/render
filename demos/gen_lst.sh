#!/usr/bin/env bash

rm gif.lst

for file in *label.png
do
  echo file $file >> gif.lst
  echo duration 1 >> gif.lst
done

vim gif.lst
