#!/bin/bash -l
#PBS -A DBIC
#PBS -q default

#PBS -j oe

#PBS -l nodes=1:ppn=16
#PBS -l walltime=96:00:00

module load singularity
cd $PBS_O_WORKDIR

BASEDIR="/idata/DBIC/castello/budapest-data-paper/scripts"
SCRIPT="run-fmriprep-discovery.sh"

CMD="$BASEDIR/$SCRIPT $SUBID"
echo "Running $CMD"
exec $CMD
