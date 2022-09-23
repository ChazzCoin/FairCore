import os

import subprocess
from F import OS

ff_AUDIO_192K = "-b:a 192k"
MP3 = ".mp3"
MP4 = ".mp4"
"192.168.1.42"
"sudo ffmpeg -re -i test.mp4 -c:v copy -c:a aac -ar 44100 -ac 1 -f flv rtmp://localhost/live/stream"

FFMPEG_TEMPLATE_simple = lambda fileIn, fileOut: f"ffmpeg -i {fileIn} {fileOut}"
FFMPEG_TEMPLATE_options = lambda fileIn, options, fileOut: f"ffmpeg -i {fileIn} {options} {fileOut}"

AUDIO_MEDIA_TYPES = [".mp3", ".mp4", ".aac", ".flac", ".m4a", ".wav", ".wma", ".ogg", ".aiff", ".alac"]
VIDEO_MEDIA_TYPES = [".mp4", ".mkv", ".mov", ".mpeg", ".wmv", ".flv", ".avi", ".webm", ".vob", ".dv", ".qt"]
ALL_MEDIA_TYPES = AUDIO_MEDIA_TYPES + VIDEO_MEDIA_TYPES

FORMAT_DV = "-vf yadif"

def clean_file_name(fileIn):
    cleanedFileIn = str(fileIn).replace(" ", "-").replace("(", "-").replace(")", "-")
    OS.rename_file(fileIn, cleanedFileIn)
    return cleanedFileIn

def to_mp3(fileIn, removeOriginal=False):
    try:
        fileIn = clean_file_name(fileIn)
        newFile = str(fileIn)[:-4]
        output = subprocess.run(f"ffmpeg -i {fileIn} -b:a 192k {newFile}{MP3}", shell=True)
        print(output)
        if removeOriginal:
            os.remove(fileIn)
        return f"{newFile}{MP3}"
    except Exception as e:
        print(f"Please make sure ffmpeg is installed!", e)
        return f"Please make sure ffmpeg is installed! error=[ {e} ]"

def to_mp4(fileIn, removeOriginal=False):
    try:
        fileIn = clean_file_name(fileIn)
        newFile = str(fileIn)[:-4]
        output = subprocess.run(f"ffmpeg -i {fileIn} -codec copy {newFile}{MP4}", shell=True)
        print(output)
        if removeOriginal:
            os.remove(fileIn)
        return f"{newFile}{MP4}"
    except Exception as e:
        print(f"Please make sure ffmpeg is installed!", e)
        return f"Please make sure ffmpeg is installed! error=[ {e} ]"