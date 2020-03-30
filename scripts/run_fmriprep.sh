#!/bin/bash -ex

IMGNAME="fmriprep-20.0.1.simg"
BASEDIR=/home/vassiki
IMG=$BASEDIR/budapest_data/singularity/$IMGNAME
WORKDIR=$BASEDIR/budapest_data/workdir
TMPDIR=$WORKDIR/tmp
DATADIR=/data/budapest/data
OUTDIR=$BASEDIR/budapest_data/outputs/
FS_LICENSE=$BASEDIR/license.txt

NCORES=24

if [ ! -d "$WORKDIR" ]; then
   echo "Creating $WORKDIR"
   mkdir -p "$WORKDIR"
fi

if [ ! -d "$TMPDIR" ]; then
   echo "Creating $TMPDIR"
   mkdir -p "$TMPDIR"
fi

if [ ! -d "$OUTDIR" ]; then
   echo "Creating $OUTDIR"
   mkdir -p "$OUTDIR"
fi

singularity run  \
  -B "$BASEDIR":"$BASEDIR" \
  -B "$WORKDIR":/work \
  -B "$DATADIR":/idata:ro \
  -B "$OUTDIR":/out \
  -e \
  "$IMG" \
  --bold2t1w-dof 6 \
  --output-spaces T1w fsaverage6 \
  --nthreads "$NCORES" \
  --omp-nthreads 8 \
  --fs-license-file "$FS_LICENSE" \
  --participant-label "$1" \
  -w /work \
  /idata /out participant \
