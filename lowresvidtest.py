from pytube import YouTube

YouTube('https://www.youtube.com/watch?v=M_-d5dsqkCE').streams.filter(res="144p", file_extension='mp4').first().download()
