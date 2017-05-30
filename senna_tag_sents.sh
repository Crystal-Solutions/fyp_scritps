#!/bin/bash
cd ../../tools/senna/
FILES=../../code/data/senna_input_sents/*.txt
OUT_DIR=../../code/data/senna_out_sents
for f in $FILES
do
  echo "Processing $f file..."
  senna -iobtags < $f > $f".out"
done
