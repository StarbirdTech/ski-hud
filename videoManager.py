# This code will manage the library of videos (in the videoSource folder) used in this project
# features:
# - keep list of currently used video in videoSource/files.json (both downloaded and not)
# - allow new videos to be added to the library by pasting a link into a cli
# - download videos from youtube and add them to the library

import os
import json
from pytube import YouTube
from pytube import Playlist
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
def addVideo(videoLink:str):
    with open('videoSource/files.json') as dataFile:
        videoData = json.loads(dataFile.read())
        for video in videoData:
            if video['link'] == videoLink:
                print('video already in library')
                return
    
    if 'playlist' in videoLink:
        playlist = Playlist(videoLink)
        for video in playlist.videos:
            addVideo(video)
        return
    
    # check if video file is in videoSource
    video = YouTube(videoLink)
    videoID = video.video_id
    videoTitle = video.title
    videoLink = videoLink
    videoFile = 'videoSource/' + videoID + '.mp4'
    if os.path.isfile(videoFile):
        print('video already in library')
        return
    else:
        try:
            video.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution().download(output_path="videoSource", filename=videoID+'.mp4')
        except:
            print('video download failed')
            return
        videoData.append({'id':videoID, 'title':videoTitle, 'link':videoLink})
        with open('videoSource/files.json', 'w') as dataFile:
            json.dump(videoData, dataFile)
        print('video added to library')

#download video given YouTube video object
def downloadVideo(video):
    videoID = video.video_id
    videoTitle = video.title
    videoLink = videoLink
    videoFile = 'videoSource/' + videoID + '.mp4'
    if os.path.isfile(videoFile):
        print('video already in library')
        return
    else:
        try:
            video.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution().download(output_path="videoSource", filename=videoID+'.mp4')
        except:
            print('video download failed')
            return
        print('video added to library')

# check if video is in library, add if not in library: input youtube video object
def checkVideo(video):
    with open('videoSource/files.json') as dataFile:
        videoData = json.loads(dataFile.read())
        for video in videoData:
            if video['id'] == video.video_id:
                print('video already in library')
                return
        downloadVideo(video)


if __name__ == '__main__':
    addVideo(input('paste video link here: '))
