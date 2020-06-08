#!/bin/bash -ex

IMGNAME="fmriprep-20.1.1.simg"
BASEDIR=/idata/DBIC/castello/budapest-data-paper
IMG=$BASEDIR/singularity/$IMGNAME
OUTDIR=$BASEDIR/outputs
WORKDIR=$OUTDIR/workdir
TMPDIR=$WORKDIR/tmp
DATADIR="$BASEDIR"
FS_LICENSE=$BASEDIR/singularity/license.txt

NCORES=16

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
  -B /idata:/idata \
  -B "$WORKDIR":/work \
  -B "$DATADIR":/data:ro \
  -B "$OUTDIR":/out \
  -e \
  "$IMG" \
   /data/data /out participant \
  --bold2t1w-dof 6 \
  --output-spaces T1w fsaverage \
  --nthreads "$NCORES" \
  --omp-nthreads 8 \
  --fs-license-file "$FS_LICENSE" \
  --participant-label "$1" \
  -w /work 
