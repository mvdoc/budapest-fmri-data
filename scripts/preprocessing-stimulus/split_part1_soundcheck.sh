#!/bin/bash
ffmpeg  \
    -i Grandbudapesthotel_HI.mkv \
    -ss 00:41:50 \
    -to 00:46:00  \
    -map 0:v -map 0:a:0 \
    -map_metadata -1 \
    -c:a aac -vbr 5 \
    -c:v libx264 -preset slow -crf 22 \
    -vf scale=720x406,setsar=1:1 \
    -copyts \
    -y \
    budapest_soundcheck.mp4
