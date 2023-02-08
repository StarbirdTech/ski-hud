# using open cv to run feature detection on all videos in video source and save to video output

import cv2 as cv
import os
import json
import concurrent.futures
import time

# run opencv feature detection on all videos in video source and save to video output

# load all videos listed in videoSource/files.json to a thread pool
# run feature detection on each video
# save output to videoOutput

# load video data
with open('videoSource/files.json') as dataFile:
    videoData = json.loads(dataFile.read())

# load all videos to a thread pool
