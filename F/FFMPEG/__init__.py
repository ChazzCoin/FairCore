import os
import subprocess

import F
from F import OS, LIST


def HandleError(e):
    print(f"Please make sure ffmpeg is installed!", e)
    return f"Please make sure ffmpeg is installed! error=[ {e} ]"

BITRATE_AUDIO_192K = "-b:a 192k"
CODEC_COPY = "-codec copy"
PNG = ".png"  # Default Image File Type
MP3 = ".mp3"  # Default Audio File Type
MP4 = ".mp4"  # Default Media (Audio/Video) Hybrid File Type
"192.168.1.42"
"sudo ffmpeg -re -i test.mp4 -c:v copy -c:a aac -ar 44100 -ac 1 -f flv rtmp://localhost/live/stream"
"ffmpeg -y -i VIDEO.mp4 -i subscribe.png -filter_complex 'overlay=x=main_w-overlay_w-(main_w*0.01):y=main_h-overlay_h-(main_h*0.01)' OUT_BOTTOM_RIGHT.mp4"
# f"ffmpeg -y -i {video_in} -i {logo_image} -filter_complex 'overlay=x=main_w-overlay_w-(main_w*0.01):y=main_h-overlay_h-(main_h*0.01)' OUT_BOTTOM_RIGHT.mp4"

FFMPEG_TEMPLATE_simple = lambda fileIn, fileOut: f"ffmpeg -i {fileIn} {fileOut}"
FFMPEG_TEMPLATE_options = lambda fileIn, options, fileOut: f"ffmpeg -i {fileIn} {options} {fileOut}"

AUDIO_MEDIA_TYPES = [".mp3", ".mp4", ".aac", ".flac", ".m4a", ".wav", ".wma", ".ogg", ".aiff", ".alac"]
VIDEO_MEDIA_TYPES = [".mp4", ".mkv", ".mov", ".mpeg", ".wmv", ".flv", ".avi", ".webm", ".vob", ".dv", ".qt"]
ALL_MEDIA_TYPES = AUDIO_MEDIA_TYPES + VIDEO_MEDIA_TYPES

# OPTIONS
NO_OPTIONS = ""
FORMAT_DV = "-vf yadif "
FORMAT_SCALE = lambda w, h: f"-vf scale={w}:{h} "
FORMAT_ADD_LOGO_bottomRight = f"-filter_complex \'overlay=x=main_w-overlay_w-(main_w*0.01):y=main_h-overlay_h-(main_h*0.01)\' "

# MAIN

FILE_IN = lambda fileIn: f"-i {fileIn} "
def FILES_IN(*filesIn):
    final = ""
    for file in filesIn:
        file = str(file).replace(",", "").replace("(", "").replace(")", "").replace("\'", "").replace("\"", "")
        final += FILE_IN(file)
    return final

BASE = "ffmpeg -y "
IN = lambda *filesIn: FILES_IN(filesIn)
OPTIONS = lambda options: f"{options} "
OUT = lambda fileOutName, fileOutType: f"{fileOutName}{fileOutType}"
FFMPEG = lambda fileIn, options, fileOut, fileOutType: f"{BASE}{IN(fileIn)}{OPTIONS(options)}{OUT(fileOut, fileOutType)}"
FFMPEG2 = lambda filesIn, options, fileOut, fileOutType: f"{BASE}{IN(filesIn)}{OPTIONS(options)}{OUT(fileOut, fileOutType)}"

""" Helpers """
def _prepare_file_name(fileIn):
    cleanedFileIn = str(fileIn).replace(" ", "-").replace("(", "-").replace(")", "-")
    OS.rename_file(fileIn, cleanedFileIn)
    return cleanedFileIn

""" Master """
def _ffmpeg(fileIn, options=NO_OPTIONS, fileOutType=MP4):
    fileIn = _prepare_file_name(fileIn)
    newFile = OS.remove_file_ext(fileIn) + "_modified"
    f_command = FFMPEG(fileIn, options, newFile, fileOutType)
    output = subprocess.run(f_command, shell=True)
    print(output)
    return newFile

def _ffmpeg2(*filesIn, options=NO_OPTIONS, fileOutType=MP4):
    firstFileIn = LIST.get(0, filesIn, False)
    fileIn = _prepare_file_name(firstFileIn)
    newFile = OS.remove_file_ext(fileIn)
    output = subprocess.run(FFMPEG(fileIn, options, newFile, fileOutType), shell=True)
    print(output)
    return newFile

""" Convenience Methods """
def is_mp3_file(fileIn):
    if F.ends_with(fileIn, ".mp3"):
        return True
    return False

def is_mp4_file(fileIn):
    if F.ends_with(fileIn, ".mp4"):
        return True
    return False

def to_mp3(fileIn, removeOriginal=False):
    if is_mp3_file(fileIn):
        print("File is already MP3")
        return None
    try:
        newFile = _ffmpeg(fileIn, NO_OPTIONS, MP3)
        if removeOriginal:
            os.remove(fileIn)
        return newFile
    except Exception as e:
        return HandleError(e)

def to_mp4(fileIn, removeOriginal=False):
    if is_mp4_file(fileIn):
        print("File is already MP4")
        return None
    try:
        newFile = _ffmpeg(fileIn, CODEC_COPY)
        if removeOriginal:
            os.remove(fileIn)
        return newFile
    except Exception as e:
        return HandleError(e)

def resize_file(fileIn, w=1920, h=1080, removeOriginal=False):
    try:
        newFile = _ffmpeg(fileIn, FORMAT_SCALE(w, h))
        if removeOriginal:
            os.remove(fileIn)
        return newFile
    except Exception as e:
        return HandleError(e)

def to_1080p(fileIn, removeOriginal=False):
    return resize_file(fileIn, removeOriginal=removeOriginal)

def to_720p(fileIn, removeOriginal=False):
    return resize_file(fileIn, w=1080, h=720, removeOriginal=removeOriginal)

def add_logo_bottom_right(fileIn, logoFile):
    return _ffmpeg2(fileIn, logoFile, options=FORMAT_ADD_LOGO_bottomRight)

# video = "/Users/chazzromeo/Desktop/logoTest/modVideo.mod"
# logo = "/Users/chazzromeo/Desktop/logoTest/thelogo.png"
# add_logo_bottom_right(video, logo)