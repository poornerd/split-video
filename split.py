#!/usr/bin/env python
import subprocess
import os
import glob
import csv
import sys
import argparse

from cleanup import cleanup               

# split files
def split(fname):
    with open(fname) as f:
        times = csv.reader(f, delimiter=';');
        line_count = 0;
        basename = os.path.splitext(os.path.basename(fname))[0] # extract base filename without extension
        for words in times:
            line_count = line_count + 1;
            print(words);
            output_filename = "part_" + basename + "_" +str(line_count).zfill(4) + "_" + words[3] + ".mov";
            highlight_filename = "part_" + basename + "_" + str(line_count).zfill(4) + "_" + words[3] + ".jpg";
            if not os.path.exists(output_filename) :
                if words[4] and words[5]:
                    arrow_cmd = ["-vf", "drawtext=text='^':enable='between(t,0,.2)':x=" + words[4] + ":y=" + words[5] + ":fontsize=166:fontcolor=red,loop=40:1,format=yuv420p"];
                else:
                    arrow_cmd = ["-vf", "loop=40:1,format=yuv420p"];
                split_cmd = ["ffmpeg", "-hwaccel", "auto", "-ss", words[1],  "-i", words[0], "-t", words[2], "-c:v", "libx264", "-s", "1920x1080"];
                reencode_cmd = ["-preset", "slow", "-crf", "20", "-c:a", "aac", "-b:a", "600k", "-movflags", "+faststart"];

                output_cmd = [ output_filename];
                # split_cmd.append(arrow_cmd);
                subprocess.check_output(split_cmd + arrow_cmd + reencode_cmd + output_cmd);

                # replicate final re-encode by adding to the split? 
                # and skip this encode?
                ## reencode_cmd = ["ffmpeg", "-i", output_filename, "-c", "copy", "-bsf:v", "h264_mp4toannexb", "-f",  "mpegts", "tmp_" + output_filename];
                ## subprocess.check_output(reencode_cmd);

                # Only extract JPG images if x and y values are present
                if words[4] and words[5]:
                    x= 960;
                    if words[4]:
                        x = int(words[4]);
                    y = 540;
                    if words[5]:    
                        y = int(words[5]);
                    highlight_cmd = ["ffmpeg","-hwaccel", "auto", "-y", "-i", output_filename, "-vf", "drawtext=text='"+str(x) + ","+str(y) +"':enable='between(t,0,.01)':x=" + str(x + 25) + ":y=" + str(y + 50) + ":fontsize=24:fontcolor=red", "-c:a", "copy", "tmp_" + output_filename];
                    subprocess.check_output(highlight_cmd);

                    extract_img_cmd = ["ffmpeg","-hwaccel", "auto",  "-i",  "tmp_" + output_filename,  "-vf", "drawtext=text='"+str(x) + ","+str(y) +"':x=" + str(x + 25) + ":y=" + str(y + 50) + ":fontsize=24:fontcolor=red", "-ss",  "00:00", "-vframes", "1",  highlight_filename];
                    subprocess.check_output(extract_img_cmd);

                    os.remove("tmp_" + output_filename); 

# create a highlight file
def create_highlight_film(name):
    filmname = "highlight_" + name + ".mov";

    for f in glob.glob(filmname):
        os.remove(f);
    file1 = open("mylist_" + name + ".txt", "w"); 
    files = sorted(list(glob.glob("part*"+name+"*.MOV"))+ list(glob.glob("part*"+name+"*.mov")));
    for item in files:
        file1.write("file %s\n" %item);
        # if item.endswith(".JPG") :
        #    file1.write("duration 1\n");   
    file1.close();

    highlight_cmd = ["ffmpeg", "-f" , "concat", "-safe", "0", "-i", "mylist_"+name+".txt", "-bsf:a", "aac_adtstoasc", "-fflags", "+genpts", "-c", "copy", filmname];
    subprocess.check_output(highlight_cmd);

    reencode_cmd = ["ffmpeg", "-hwaccel", "auto", "-y", "-i", filmname, "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-c:a", "aac", "-b:a", "600k", "-vf", "format=yuv420p", "-movflags", "+faststart", "final_" + filmname];
    subprocess.check_output(reencode_cmd);

##cleanup();
parser = argparse.ArgumentParser()
parser.add_argument('input_filename', nargs='?', default='default.csv', help='Input file name')
parser.add_argument('--reel_type', default='highlight', help='Reel type', required=False)
parser.add_argument('--clean', action='store_true', help='Clean up before processing', required=False)
parser.add_argument('--only_clean', action='store_true', help='Only clean up', required=False)

args = parser.parse_args()

if args.only_clean:
    cleanup()
    sys.exit()
elif args.clean:
    cleanup()

input_filename = args.input_filename
split(input_filename);

if args.reel_type:
    reel_type = args.reel_type
    create_highlight_film(reel_type);

