#!/usr/bin/env python

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

with open("input.txt") as f:
  times = f.readlines()

for time in times:
    print(time)
