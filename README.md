

[![DOI](https://zenodo.org/badge/251371344.svg)](https://zenodo.org/badge/latestdoi/251371344)


# An fMRI dataset in response to "The Grand Budapest Hotel", a socially-rich, naturalistic movie

This repository contains code related to the fMRI dataset collected while participants watched [The Grand BudapestHotel](https://en.wikipedia.org/wiki/The_Grand_Budapest_Hotel) by Wes Anderson. The associated manuscript *An fMRI dataset in response to "The Grand Budapest Hotel", a socially-rich, naturalistic movie* by Matteo Visconti di Oleggio Castello, Vassiki Chauhan, Guo Jiahui, & M. Ida Gobbini is available as a preprint [here](https://www.biorxiv.org/content/10.1101/2020.07.14.203257v1).

If you use the dataset, please cite the corresponding preprint:

Visconti di Oleggio Castello, M., Chauhan, V., Jiahui, G., & Gobbini, M. I. (2020). *An fMRI dataset in response to "The Grand Budapest Hotel", a socially-rich, naturalistic movie*. In bioRxiv (p. 2020.07.14.203257). https://doi.org/10.1101/2020.07.14.203257

The dataset is available on OpenNeuro: https://openneuro.org/datasets/ds003017. See below for information on how to install the dataset.

This repository can be cited as follows

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

In this repository we provide the scripts used to generate and preprocess the stimuli, to present the stimuli in the scanner, to preprocess the fMRI data, and to run quality assurance analyses. These scripts can be found in the directory [scripts](scripts). In particular,

- [scripts/preprocessing-stimulus](scripts/preprocessing-stimulus) contains the scripts to
  split the movie into separate parts to be presented in the scanner, and preprocess the audio of the movie to make it more audible in the scanner.
- [scripts/presentation](scripts/presentation) contains PsychoPy presentation scripts.
- [scripts/preprocessing-fmri](scripts/preprocessing-fmri) contains the scripts used to run [fMRIprep](https://fmriprep.readthedocs.io/) for preprocessing.
- [scripts/quality-assurance](scripts/quality-assurance) contains scripts to run QA analyses and generate the figures reported in the data paper.
- [scripts/hyperalignment-and-decoding](hyperalignment-and-decoding) contains scripts to perform hyperalignment and movie segment classification.

Below we describe these scripts in more detail.

### Stimulus preprocessing

- `split_movie_behav.sh` splits and preprocess the first
  part of the movie, which subjects watched outside the scanner.
- `split_movie.sh` splits and preprocess the second part of the movie,
  which subjects watched divided into five parts in the scanner.
- `split_part1_soundcheck.sh` extracts the last five minutes of the
  first part of the movie. This part was shown during the anatomical
  scan so that subjects could adjust the volume.
- `splits_behav.txt` contains the timing for the first part.
- `splits.txt` contains the timing for the second part, with each row
  indicating a split.

### Presentation scripts

### fMRI preprocessing with fMRIprep

### Quality assurance scripts

### Hyperalignment and decoding scripts

## Notebooks