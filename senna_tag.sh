#!/bin/bash
cd ../../tools/senna/
FILES=../../code/data/senna_input_sents/*.txt
OUT_DIR=../data/senna_out/
for f in $FILES
do
  echo "Processing $f file..."
  # take action on each file. $f store current file name
  #cat $f
  senna -iobtags < $f > $f".out"
done
