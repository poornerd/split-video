import glob, os, subprocess

# create a highlight file
def create_highlight_film(reel_type):
    filmname = "highlight_" + reel_type + ".mov";

    for f in glob.glob(filmname):
        os.remove(f);
    file1 = open("mylist_" + reel_type + ".txt", "w"); 
    files = sorted(list(glob.glob("part*"+reel_type+"*.MOV"))+ list(glob.glob("part*"+reel_type+"*.mov")));
    for item in files:
        file1.write("file %s\n" %item);
        # if item.endswith(".JPG") :
        #    file1.write("duration 1\n");   
    file1.close();

    highlight_cmd = ["ffmpeg", "-f" , "concat", "-safe", "0", "-i", "mylist_"+reel_type+".txt", "-bsf:a", "aac_adtstoasc", "-fflags", "+genpts", "-c", "copy", filmname];
    subprocess.check_output(highlight_cmd);

    reencode_cmd = ["ffmpeg", "-hwaccel", "auto", "-y", "-i", filmname, "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-c:a", "aac", "-b:a", "600k", "-vf", "format=yuv420p", "-movflags", "+faststart", "final_" + filmname];
    subprocess.check_output(reencode_cmd);