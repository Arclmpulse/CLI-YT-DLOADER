from pytube import YouTube
import yt_dlp
import os
from pathlib import Path

def VideoTitle(url):
    try:
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get('title', 'Unknown Title')

    except Exception as e:
        print(f"Error retrieving video title: {e}")
        return 'Unknown Title'

def downloadVideo(url, file_Type='mp4'):
    try:
        video_title = VideoTitle(url)
        print(f"Title: {video_title}")
        filename = input("Enter Filename (Blank Defaults to Video Title): ").strip()
        if not filename:
            filename = video_title

        defDLPath = str(Path.home() / "Downloads")
        dlPath = input(f"Enter Download Path (blank for default): ")
        if not dlPath:
            dlPath = defDLPath
        os.makedirs(dlPath, exist_ok=True)
        
        yt = YouTube(url)

        if file_Type == 'mp4':
            print("\nAvailable Resolutions:")
            streams = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc()
            resolutions = [stream.resolution for stream in streams]
            for i, res in enumerate(resolutions, start=1):
                print(f"{i}, {res}")
            
            resChoice = int(input("\nSelect Resolution (Number): ").strip())
            stream = streams[resChoice - 1]


            stream.download(output_path=dlPath, filename = f"{filename}.mp4")
            print(f"Downloaded Successfully as '{filename}.mp4'.")

        elif file_Type == "mp3":
            stream = yt.streams.filter(only_audio=True).first()
            dlFile = stream.download(output_path=dlPath, filename=f"{filename}.mp4")

            baseFile, _ = dlFile.rsplit('.', 1)
            mp3File = f"{baseFile}.mp3"
            os.rename(dlFile, mp3File)
            print(f"Downloaded Successfully as '{filename}.mp3'.")

        else:
            print("Invalid Filetype. Try again.")

    except Exception as e:
        print(f"An error occured: {e}")

if __name__ == "__main__":
    videoURL = input("Enter YouTube URL: ").strip()
    fileType = input("Enter File Type (mp3/mp4): ").strip().lower()
    downloadVideo(videoURL, fileType)