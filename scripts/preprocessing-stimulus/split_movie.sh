#!/bin/bash
p=2
#-vf pad=720:540:0:30,setdar=dar=4/3 \

while read -r start stop; do
  echo Start: $start Stop: $stop
  ffmpeg  \
    -i Grandbudapesthotel_HI.mkv \
    -ss "$start" \
    -to "$stop" \
    -map 0:v -map 0:a:0 \
    -map_metadata -1 \
    -af compand="0|0:1|1:-90/-900|-70/-70|-30/-9|0/-3:6:0:0:0" \
    -c:a aac -vbr 5 \
    -c:v libx264 -preset slow -crf 22 \
    -vf scale=720x406,setsar=1:1 \
    -copyts \
    -y \
    budapest_part"$p".mp4 < /dev/null
  p=$[p + 1]
done < splits.txt
