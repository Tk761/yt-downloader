#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
if [ ! -d "ffmpeg_dir" ]; then
  mkdir -p ffmpeg_dir
  curl -L https://github.com/ffbinaries/ffbinaries-prebuilt/releases/download/v4.4.1/ffmpeg-4.4.1-linux-64.zip -o ffmpeg.zip
  unzip ffmpeg.zip -d ffmpeg_dir
  rm ffmpeg.zip
  chmod +x ffmpeg_dir/ffmpeg
fi
