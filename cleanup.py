import glob, os

def cleanup():
    for f in glob.glob("part*.MOV"):
        os.remove(f)
    for f in glob.glob("part*.mov"):
        os.remove(f)        
    for f in glob.glob("tmp_part*.MOV"):
        os.remove(f)
    for f in glob.glob("tmp_part*.mov"):
        os.remove(f)
    for f in glob.glob("part*.JPG"):
        os.remove(f)  
    for f in glob.glob("part*.jpg"):
        os.remove(f)
