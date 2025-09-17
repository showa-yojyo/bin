#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

declare -ar ffprobe_options=(
    -hide_banner
    -v error
    -show_entries "format=duration"
    -of "default=noprint_wrappers=1:nokey=1")

declare -a durations
for i in *.mp4 ; do
    durations+=($(ffprobe "${ffprobe_options[@]}" "$i"))
done

sum=$(echo ${durations[0]} - 1 | bc)
echo $sum
for ((i=1; i<${#durations[@]}; i++)); do
    sum=$(echo $sum + ${durations[i]} - 1 | bc)
    echo $sum
done
