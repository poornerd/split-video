
# Split Video script

This is a shell script to split a video - for example for soccer - into multiple highlight clips based on a text file containing the start and end times.

The script generates a highlight video, as well as a video with all goals.


## Install
In order for this to work (only tested on OSX 10.15) you need to install ffmpeg, glew and glfw for example:
```
brew install glew glfw
brew install ffmpeg $(brew options ffmpeg | grep -vE '\s' | grep -- '--with-' | tr '\n' ' ')
```

## How to use
First create an input file called ```input.txt``` with one line per clip to split / cut out of the larger video.  The format is like:
```
 filname.mov start-time length clip-filename.mov
 filname.mov start-time length clip-filename.mov
 filname.mov start-time length clip-filename.mov 
```

An *example* would be:
```
 IMG_9651.MOV 00:24 00:04 part_01_dribble.MOV
 IMG_9651.MOV 01:57 00:06 part_02_goal.MOV
 IMG_9651.MOV 09:12 00:05 part_03_shot.MOV
 IMG_9651.MOV 10:20 00:06 part_04_dribble.MOV
 IMG_9652.MOV 04:39 00:05 part_05_goal.MOV
 IMG_9654.MOV 00:20 00:06 part_06_goal.MOV
 IMG_9654.MOV 00:52 00:04 part_07_pass.MOV
 IMG_9654.MOV 03:03 00:04 part_08_pass.MOV
 IMG_9655.MOV 09:43 00:20 part_09_dribble.MOV
 
```

**It is important to follow the naming convention for the clips!**
- starts with "part"
- followed by "_XX_" - a number preceeded by 0 so that when the files are sorted they are in the right order
- a keyword(s) which describes the clip, with "_" for spaces.  The only relevant keyword is **goal** because those clips get added to a separate highlight video of just goals.