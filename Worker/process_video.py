import os
from bucket import upload_file
from update_video_db import update_video_status
# from celery import Celery

import argparse
import typing
from typing import Optional

if typing.TYPE_CHECKING:
    from google.pubsub_v1 import types as gapic_types

# celery_app = Celery('task', broker='redis://localhost:6379/0')
# actual_dir = os.path.dirname(os.path.abspath(__file__))
actual_dir = "."
base_dir = os.path.join(actual_dir, "Processing")
editing_dir = os.path.join(actual_dir, "Processing", "Editing")
processed_dir = os.path.join(actual_dir, "Processing", "Processed")

downloaded_blob = "Downloaded"
processed_blob = "Processed"

url_logo = "https://raw.githubusercontent.com/gsgomezm/MISW4204-SWNube-MEG/main/VideosFpv/Editing/logo.mp4"

# debconf: delaying package configuration, since apt-utils is not installed
# WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv

# @celery_app.task()
def process_video(video_id, url_video):
    try:
        create_dirs()
        parts = url_video.split("/")
        video_filename = parts[-1]
        parts = video_filename.split(".mp4")
        name = parts[0]
        download_video(url_video, video_filename)
        file_concat_path = create_file_conc(name, video_filename)
        edit_video(video_filename, file_concat_path)
        remove_file("Editing", name + ".txt")
        remove_file("Editing", video_filename)
        remove_file("Editing", "c_" + video_filename)
        remove_file("Editing", "l_" + video_filename)
        remove_file("Processed", video_filename)
        update_video_status(video_id, "processed")
    except OSError as e:
        print(f"Error: {e.strerror}")

def edit_video(video_filename, file_concat_path):
    file_path = os.path.join(editing_dir, video_filename)
    file_c = os.path.join(editing_dir, "c_" + video_filename)
    file_l = os.path.join(editing_dir, "l_" + video_filename)
    file_p = os.path.join(processed_dir, video_filename) 
    # destiny_path = os.path.join(actual_dir, "VideosFpv")
    processed_blob_file = processed_blob + "/" + video_filename
    os.system('ffmpeg -f concat -safe 0 -i "' + file_concat_path + '" -c copy -movflags faststart "' + file_c + '"')
    os.system('ffmpeg -ss 0 -t 20  -i "' + file_c + '" -c copy -movflags faststart "' + file_l + '"')
    os.system('ffmpeg -i "' + file_l + '" -c copy -aspect 16/9 "' + file_p + '"')
    # os.system(f"{file_path} {destiny_path}")
    upload_file(processed_blob_file, file_p)

def download_video(url_video, video_name):
    video_editing = os.path.join(editing_dir, video_name)
    video_logo = os.path.join(editing_dir, "logo.mp4")
    downloaded_blob_file = downloaded_blob + "/" + video_name
    os.system(f"curl -o {video_editing} {url_video}")
    if not os.path.exists(video_logo):
        os.system(f"curl -o {video_logo} {url_logo}") 
    upload_file(downloaded_blob_file, video_editing)
    
def create_file_conc(video_name, file_name):
    file_path = os.path.join(editing_dir, video_name + ".txt")
    content = "file logo.mp4\n" + "file " + file_name + "\n" + "file logo.mp4"
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write(content)
            file.close()
    return file_path

def remove_file(folder_name, filename):
    file = os.path.join(base_dir, folder_name, filename)
    if  os.path.exists(file):
        os.system(f"rm {file}")

def create_dirs():
    if not os.path.exists(base_dir):
        os.system(f"mkdir -p {base_dir}")
    if not os.path.exists(editing_dir):
        os.system(f"mkdir -p {editing_dir}")
    if not os.path.exists(processed_dir):
        os.system(f"mkdir -p {processed_dir}")
