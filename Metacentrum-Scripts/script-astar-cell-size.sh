#!/bin/bash
#PBS -l walltime=3:00:00
#PBS -l select=1:ncpus=1:mem=4gb:scratch_local=1gb:cluster=adan
#PBS -e /storage/praha1/home/hribljaa/job_logs
#PBS -o /storage/praha1/home/hribljaa/job_logs

DATADIR=/storage/praha1/home/hribljaa/super-mario-astar
RESULTDIR=/storage/praha1/home/hribljaa/results/cellsize
ROOT=/storage/praha1/home/hribljaa

echo "$PBS_JOBID is running on node `hostname -f` in a scratch directory $SCRATCHDIR" >> $ROOT/jobs_info.txt

module add openjdk-17

test -n "$SCRATCHDIR" || { echo >&2 "Variable SCRATCHDIR is not set!"; exit 1; }

cp -R $DATADIR/Mario-AI-Framework $SCRATCHDIR || { echo >&2 "Error while copying input file(s)!"; exit 2; }

cd $SCRATCHDIR/Mario-AI-Framework

javac -cp src src/mff/agents/benchmark/AstarCellSizeBenchmark.java
java -cp src mff.agents.benchmark.AstarCellSizeBenchmark $CELL_SIZE $TTFW

mkdir -p $RESULTDIR
cp -a agent-benchmark/. $RESULTDIR/ || { echo >&2 "Error while copying output file(s) to result dir!"; exit 2; }

clean_scratch
