# Scripts used to preprocess the stimulus

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
