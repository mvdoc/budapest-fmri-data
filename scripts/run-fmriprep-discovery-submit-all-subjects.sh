#!/bin/bash

SCRIPT="run-fmriprep-discovery-submit.pbs"

for SUBID in ../data/sub-*; do
    SUBID=$(basename "$SUBID")
    SUBID="${SUBID##*\-}"
	echo "Submitting job for sub-"$SUBID""
    	qsub -v SUBID="$SUBID" -o logs/fmriprep-"$SUBID".out "$SCRIPT"
	echo ""
done
