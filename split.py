#!/usr/bin/env python
import subprocess
import os
import glob
import csv
import sys

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
    for f in glob.glob("tmp_part*.JPG"):
        os.remove(f);          

# split files
def split(fname):
    with open(fname) as f:
        times = csv.reader(f, delimiter=';');
        line_count = 0;
        for words in times:
            line_count = line_count + 1;
            print(words);
            output_filename = "part_" + str(line_count).zfill(4) + "_" + words[3] + ".MOV";
            if not os.path.exists(output_filename) :
                if words[4] and words[5]:
                    arrow_cmd = ["-vf", "drawtext=text='^':enable='between(t,0,.3)':x=" + words[4] + ":y=" + words[5] + ":fontsize=66:fontcolor=red,loop=40:1"];
                else:
                    arrow_cmd = ["-vf", "loop=40:1"];
                split_cmd = ["ffmpeg", "-ss", words[1],  "-i", words[0], "-t", words[2], "-c:v", "libx264", "-s", "1920x1080"];
                output_cmd = [ output_filename];
                # split_cmd.append(arrow_cmd);
                subprocess.check_output(split_cmd + arrow_cmd + output_cmd);
                # highlight_cmd = ["ffmpeg", "-y", "-i", output_filename, "-vf", "drawtext=text='^':x=1140:y=260:fontsize=66:fontcolor=red", "-c:a", "copy", "O_" + output_filename];
                # subprocess.check_output(highlight_cmd);
                reencode_cmd = ["ffmpeg", "-i", output_filename, "-c", "copy", "-bsf:v", "h264_mp4toannexb", "-f",  "mpegts", "tmp_" + output_filename];
                subprocess.check_output(reencode_cmd);

# create the highlight file
def create_highlight_film():
    for f in glob.glob("highlight.MOV"):
        os.remove(f);
    file1 = open("mylist_all.txt", "w"); 
    files = sorted(list(glob.glob("tmp_part*.MOV")) + list(glob.glob("tmp_part*.mov"))); # concat list with lower case?
    for item in files:
        file1.write("file %s\n" %item);
    file1.close();

    highlight_cmd = ["ffmpeg", "-f" , "concat", "-safe", "0", "-i", "mylist_all.txt", "-bsf:a", "aac_adtstoasc", "-fflags", "+genpts", "-c", "copy", "highlight.MOV"];
    subprocess.check_output(highlight_cmd);


# create the highlight file
def create_goals_film():
    for f in glob.glob("goals.MOV"):
        os.remove(f);
    file1 = open("mylist_goal.txt", "w"); 
    files = sorted(list(glob.glob("tmp_part*goal*.MOV"))+ list(glob.glob("tmp_part*goal*.mov")));
    for item in files:
        file1.write("file %s\n" %item);
    file1.close();

    goals_cmd = ["ffmpeg", "-f" , "concat", "-safe", "0", "-i", "mylist_goal.txt", "-bsf:a", "aac_adtstoasc", "-fflags", "+genpts", "-c", "copy", "goals.MOV"];
    subprocess.check_output(goals_cmd);

# create a highlight file
def create_highlight_film(name):
    filmname = "highlight_" + name + ".mov";

    for f in glob.glob(filmname):
        os.remove(f);
    file1 = open("mylist_" + name + ".txt", "w"); 
    files = sorted(list(glob.glob("tmp_part*"+name+"*.MOV"))+ list(glob.glob("tmp_part*"+name+"*.mov")));
    for item in files:
        file1.write("file %s\n" %item);
        # if item.endswith(".JPG") :
        #    file1.write("duration 1\n");   
    file1.close();

    goals_cmd = ["ffmpeg", "-f" , "concat", "-safe", "0", "-i", "mylist_"+name+".txt", "-bsf:a", "aac_adtstoasc", "-fflags", "+genpts", "-c", "copy", filmname];
    subprocess.check_output(goals_cmd);

    reencode_cmd = ["ffmpeg", "-y", "-i", filmname, "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-c:a", "aac", "-b:a", "160k", "-vf", "format=yuv420p", "-movflags", "+faststart", "final_" + filmname];
    subprocess.check_output(reencode_cmd);

##cleanup();
if sys.argv[1]:
    param_1= sys.argv[1];
    if param_1 == "clean":
        cleanup();
        if sys.argv[2]:
            input_filename= sys.argv[2];
    else:
        input_filename = param_1;

split(input_filename);
create_highlight_film("highlight");
##create_goals_film();
##create_highlight_film("nicholas");
##create_highlight_film("team");