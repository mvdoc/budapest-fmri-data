

[![DOI](https://zenodo.org/badge/251371344.svg)](https://zenodo.org/badge/latestdoi/251371344)


# An fMRI dataset in response to "The Grand Budapest Hotel", a socially-rich, naturalistic movie

This repository contains code related to the fMRI dataset collected while participants watched [The Grand BudapestHotel](https://en.wikipedia.org/wiki/The_Grand_Budapest_Hotel) by Wes Anderson. The associated manuscript *An fMRI dataset in response to "The Grand Budapest Hotel", a socially-rich, naturalistic movie* by Matteo Visconti di Oleggio Castello, Vassiki Chauhan, Guo Jiahui, & M. Ida Gobbini is available as a preprint [here](https://www.biorxiv.org/content/10.1101/2020.07.14.203257v1).

If you use the dataset, please cite the corresponding preprint:

Visconti di Oleggio Castello, M., Chauhan, V., Jiahui, G., & Gobbini, M. I. (2020). *An fMRI dataset in response to "The Grand Budapest Hotel", a socially-rich, naturalistic movie*. In bioRxiv (p. 2020.07.14.203257). https://doi.org/10.1101/2020.07.14.203257

The dataset is available on OpenNeuro: https://openneuro.org/datasets/ds003017. See below for information on how to install the dataset.

This repository can be cited as follows:

Visconti di Oleggio Castello, M., Chauhan,  V., Jiahui, G., & Gobbini, M. I. (2020).  *mvdoc/budapest-fmri-data: v0.0.1 (Version v0.0.1)*. Zenodo.  http://doi.org/10.5281/zenodo.3942174

## Dataset download

The dataset can be downloaded from [OpenNeuro, dataset ds003017]( https://openneuro.org/datasets/ds003017). Alternatively, it can be downloaded using [DataLad](https://www.datalad.org/). Once DataLad is installed in your system, the dataset can be installed as follows

```bash
$ datalad install ///labs/gobbini/budapest/openneuro
```

Please refer to the [DataLad handbook](http://handbook.datalad.org/en/latest/) to learn how to use DataLad.

## Setting up a python environment

We provide a conda environment file to set up an appropriate python environment for the preprocessing scripts. This environment has been tested on Linux and Mac OS X, however there's a chance it might not work on your system. Please feel free to open an issue here and we'll try to help.

Assuming you have already installed [anaconda or miniconda](https://docs.anaconda.com/anaconda/install/) on your system, you can set up a new conda environment with requirements as follows (note that it can take a while):

```bash
$ conda env create -f conda-environment.yml --name budapest
```

Once all packages have been installed, you should activate the environment and install an additional python package that we provide which contains additional helper functions:

```bash
$ conda activate budapest
$ pip install ./code
```

## Presentation, preprocessing, and quality assurance scripts

In this repository we provide the scripts used to generate and preprocess the stimuli, to present the stimuli in the scanner, to preprocess the fMRI data, and to run quality assurance analyses. These scripts can be found in the [`scripts`](scripts) directory. In particular,

- [scripts/preprocessing-stimulus](scripts/preprocessing-stimulus) contains the scripts to
  split the movie into separate parts to be presented in the scanner, and preprocess the audio of the movie to make it more audible in the scanner.
- [scripts/presentation](scripts/presentation) contains PsychoPy presentation scripts.
- [scripts/preprocessing-fmri](scripts/preprocessing-fmri) contains the scripts used to run [fMRIprep](https://fmriprep.readthedocs.io/) for preprocessing.
- [scripts/quality-assurance](scripts/quality-assurance) contains scripts to run QA analyses and generate the figures reported in the data paper.
- [scripts/hyperalignment-and-decoding](hyperalignment-and-decoding) contains scripts to perform hyperalignment and movie segment classification.

Below we describe the content of these directories in more detail.

### Stimulus preprocessing

The movie was extracted from a DVD and converted into mkv (`libmkv 0.6.5.1`) format using [HandBrake](https://handbrake.fr/). Unfortunately, this process was not scripted. The DVD had [UPC code 024543897385](https://www.upcitemdb.com/upc/24543897385). We provide additional metadata associated with the converted movie file to make sure that future conversions would match our stimuli as best as possible. The information is available in [`scripts/preprocessing-stimulus/movie-file-info.txt`](scripts/preprocessing-stimulus/movie-file-info.txt). In particular, the total video duration was `01:39:55.17`. The video and audio were encoded with the following codecs:

```
Stream #0:0(eng): Video: h264 (High), yuv420p(tv, smpte170m/smpte170m/bt709, progressive), 720x480 [SAR 32:27 DAR 16:9], SAR 186:157 DAR 279:157, 30 fps, 30 tbr, 1k tbn, 60 tbc (default)
Stream #0:1(eng): Audio: ac3, 48000 Hz, stereo, fltp, 160 kb/s (default)
Stream #0:2(eng): Audio: ac3, 48000 Hz, 5.1(side), fltp, 384 kb/s
```

Once the movie was extracted and converted, it was split into different parts for a behavioral session and five imaging runs. The timing of the first, behavioral session is available in [`scripts/preprocessing-stimulus/splits_behav.txt`](scripts/preprocessing-stimulus/splits_behav.txt). These first ~45 minutes of the movie were shown outside the scanner, right before the imaging session. The timings of the five additional splits of the second part of the movie are available in [`scripts/preprocessing-stimulus/splits.txt`](scripts/preprocessing-stimulus/splits.txt). Each row indicates a pair of start/end times for each subclip.

We also provide the scripts used to generate these splits, which used `ffmpeg`. While the movies were converted, the audio was also postprocessed and passed through an audio compressor to reduce the dynamic range and make dialogues more audible in the scanner. These scripts are  [`scripts/preprocessing-stimulus/split_movie_behav.sh`](scripts/preprocessing-stimulus/split_movie_behav.sh) and [`scripts/preprocessing-stimulus/split_movie.sh`](scripts/preprocessing-stimulus/split_movie.sh) for the behavioral and imaging sessions respectively. They will produce six files named `budapest_part[1-6].mp4` that were used for the experiment.

Finally, while an anatomical scan was acquired, subjects were shown the last five minutes of `budapest_part1.mp4` so that they could select an appropriate volume for the remaining five scans. The clip showed during the anatomical scan is generated by the script [`scripts/preprocessing-stimulus/split_part1_soundcheck.sh`](scripts/preprocessing-stimulus/split_part1_soundcheck). This script will generate a file named `budapest_soundcheck.mp4`. 

### Presentation scripts

### fMRI preprocessing with fMRIprep

### Quality assurance scripts

### Hyperalignment and decoding scripts

## Notebooks