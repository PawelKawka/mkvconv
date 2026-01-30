# mkvconv

A lightweight Python CLI utility for converting MKV video files to MP4

## Required 

- python3
- ffmpeg

 ## Usage

 - To run use:
```bash
python3 mkvconv.py examplefile.mkv
```

## Arguments

- **--slow**: Enable re-encoding mode. Use this if you need to compress the file **[Default: Disabled]**
- **-c, --crf**: Quality (0–51). Lower value means better quality. Works only in --slow mode **Default: 23]**
- **-p, --preset**: Encoding speed (e.g. fast, medium, slow). Works only in --slow mode **[Default: medium]**



## About

- Uses libx264 for video and AAC for audio.
- Developed and tested on Linux, no promise it will work on Windows.
