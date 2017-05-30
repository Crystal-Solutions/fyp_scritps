#!/bin/bash
cd ../../tools/senna/
FILES=../../code/data/senna_input_resps/*.txt
OUT_DIR=../../code/data/senna_out_resps
for f in $FILES
do
  echo "Processing $f file..."
  senna -iobtags < $f > $f".out"
done
