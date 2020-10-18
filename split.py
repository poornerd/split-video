#!/usr/bin/env python
import subprocess
import os
import glob

# cleanup
def cleanup():
    for f in glob.glob("part*.MOV"):
        os.remove(f);
    for f in glob.glob("part*.mov"):
        os.remove(f);        
    for f in glob.glob("tmp_part*.MOV"):
        os.remove(f);
    for f in glob.glob("tmp_part*.mov"):
        os.remove(f);

# split files
def split(fname):
    with open(fname) as f:
        times = f.readlines()
    for time in times:
        words = time.split();
        print(words[1]);
        split_cmd = ["ffmpeg", "-ss", words[1], "-i", words[0], "-t", words[2], "-c", "copy", words[3]];
        subprocess.check_output(split_cmd);
        reencode_cmd = ["ffmpeg", "-i", words[3], "tmp_" + words[3]]
        subprocess.check_output(reencode_cmd);


# create the highlight file
def create_highlight_film():
    for f in glob.glob("highlight.MOV"):
        os.remove(f);
    file1 = open("mylist.txt", "w"); 
    files = sorted(list(glob.glob("tmp_part*.MOV")) + list(glob.glob("tmp_part*.mov"))); # concat list with lower case?
    for item in files:
        file1.write("file %s\n" %item);
    file1.close();

    highlight_cmd = ["ffmpeg", "-f" , "concat", "-safe", "0", "-i", "mylist.txt", "-bsf:a", "aac_adtstoasc", "-fflags", "+genpts", "-c", "copy", "highlight.MOV"];
    subprocess.check_output(highlight_cmd);


# create the highlight file
def create_goals_film():
    for f in glob.glob("goals.MOV"):
        os.remove(f);
    file1 = open("mylist.txt", "w"); 
    files = sorted(list(glob.glob("tmp_part*goal*.MOV"))+ list(glob.glob("tmp_part*goal*.mov")));
    for item in files:
        file1.write("file %s\n" %item);
    file1.close();

    highlight_cmd = ["ffmpeg", "-f" , "concat", "-safe", "0", "-i", "mylist.txt", "-bsf:a", "aac_adtstoasc", "-fflags", "+genpts", "-c", "copy", "goals.MOV"];
    subprocess.check_output(highlight_cmd);

cleanup();
split("input.txt");
create_highlight_film();
create_goals_film();