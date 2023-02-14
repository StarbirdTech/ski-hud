from pytube import YouTube
import os

def downloadVideo(videoLink:str):
    video = YouTube(videoLink)
    if os.path.isfile('videoSource/' + video.video_id + '.mp4'):
        print('video already in library')
        return
    else:
        try:
            video.streams.filter(progressive=True, file_extension='mp4', res='720p').first().download(output_path="videoSource", filename=video.video_id+'.mp4')
        except:
            print('video download failed')
            return
        print('video added to library')

if __name__ == "__main__":
    downloadVideo('https://www.youtube.com/watch?v=lo6rBzkYw14')