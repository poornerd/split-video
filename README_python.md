# Python Split Video

This code is used to split a video into multiple parts based on a CSV file with specified timecodes, create a highlight reel by concatenating selected parts, add a text overlay, and extract a still image from each part.


## Installation

### FFmpeg

#### MacOS: 
```
brew install ffmpeg
```

#### Linux: 
```
sudo apt-get install ffmpeg
```

### Python libraries

Install the required Python libraries using the following command:
```
pip install argparse
```

## Usage

Run the following command to use the program:

```
python filename.py [-h] [--reel_type REEL_TYPE] [--clean] [--only_clean] [input_filename]

input_filename - (optional) The CSV file with timecodes for splitting the video.

--reel_type - (optional) The type of reel to create: 'highlight' is the default value.

--clean - (optional) Remove all previously created files.

--only_clean - (optional) Remove all previously created files and exit the program.
```

## Functionality


split(fname) - Splits the video based on the CSV file provided and adds a text overlay and extracts a still image from each part.

create_highlight_film(name) - Concatenates selected parts to create a highlight reel.
