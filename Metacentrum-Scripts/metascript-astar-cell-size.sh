#!/bin/bash

for cs in 1 2 3 4 5 6 8 10 12 16
do
  for ttfw in 0.2 0.4 0.6 0.8 1.0 1.2 1.4 1.6 1.8 2.0
  do
    echo $cs $ttfw
    qsub -v CELL_SIZE=$cs,TTFW=$ttfw script-astar-cell-size.sh
  done
done
