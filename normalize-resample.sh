#!/usr/bin/env bash
# copy this to root directory of data and ./normalize-resample.sh
# https://unix.stackexchange.com/questions/103920/parallelize-a-bash-for-loop

open_sem(){
    mkfifo pipe-$$
    exec 3<>pipe-$$
    rm pipe-$$
    local i=$1
    for((;i>0;i--)); do
        printf %s 000 >&3
    done
}
run_with_lock(){
    local x
    read -u 3 -n 3 x && ((0==x)) || exit $x
    (
     ( "$@"; )
    printf '%.3d' $? >&3
    )&
}

current_pwd="${PWD}"
sub_folder=${current_pwd##*/}
echo ${sub_folder}

resulted_path="Normalized_data"

cd ../
mkdir -p ${resulted_path}
target_folder="${PWD}/${resulted_path}"
echo ${target_folder}

cd ${sub_folder}
echo ${PWD}

N=7 # set "N" as your CPU core number.
open_sem $N
find . -type f -name "*.flac" -print0 | while IFS= read -r -d '' file; do
    echo "file = $file"
    file_folder=${file}
    cleaned_file_folder="${target_folder}/${file_folder:2}"
    echo "${cleaned_file_folder%/*}"
    mkdir -p "${cleaned_file_folder%/*}"
    run_with_lock ffmpeg-normalize "$file" -ar 16000 -f -o "${cleaned_file_folder%.*}-norm.wav"
done

# N=7 # set "N" as your CPU core number.
# open_sem $N
# for f in $(find . -name "*.flac"); do
#     file_folder=${f}
#     cleaned_file_folder="${target_folder}/${file_folder:2}"
#     echo "${cleaned_file_folder%/*}"
#     mkdir -p "${cleaned_file_folder%/*}"
# #    ffmpeg-normalize "$f" -ar 16000 -o "${cleaned_file_folder%.*}-norm.wav"
# #    ffmpeg-normalize "$f" -ar 16000 -o "${cleaned_file_folder%.*}-norm.wav"
#     # run_with_lock ffmpeg-normalize "$f" -ar 16000 -f -o "${cleaned_file_folder%.*}-norm.wav"
# done