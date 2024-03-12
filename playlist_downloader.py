import os
from pytube import Playlist


def make_alpha_numeric(string):
    return "".join(char for char in string if char.isalnum())


link = input("Enter YouTube Playlist URL: ").strip()

yt_playlist = Playlist(link)

folderName = make_alpha_numeric(yt_playlist.title)

# Create the download folder if it doesn't exist
os.makedirs(yt_playlist.title, exist_ok=True)

totalVideoCount = len(yt_playlist.videos)
print("Total videos in playlist: 🎦", totalVideoCount)

downloaded_files = os.listdir(f"./{folderName}")

# Extract downloaded video titles from the filenames
downloaded_titles = set()
for filename in downloaded_files:
    if filename.endswith(".mp4"):
        title = os.path.splitext(filename)[0].split("-", 1)[-1].strip()
        print(title)
        downloaded_titles.add(title)


def download_vid(video_stream, resolution):
    video_size = video_stream.filesize
    print(f"Size: {video_size // (1024**2)} MB \t Resolution: {resolution}")
    video_stream.download(output_path=folderName, filename=f"{index}-{video.title}.mp4")
    print("Downloaded:", video.title, "✨ successfully!")
    print("Remaining Videos:", totalVideoCount - index)


for index, video in enumerate(yt_playlist.videos, start=1):
    title = video.title
    if title in downloaded_titles:
        print(f"Skipping {title} - Already downloaded")
        continue
    try:
        print("Downloading:", video.title)

        video_stream = video.streams.get_by_resolution("360p")
        if video_stream:
            download_vid(video_stream, "360p")
        else:
            video_stream = video.streams.get_by_resolution("480p")
            if video_stream:
                download_vid(video_stream, "480p")
            else:
                video_stream = video.streams.get_highest_resolution()
                download_vid(video_stream, "highest resolution")
    except Exception as e:
        print(f"Failed to download {title}: {e}")

print("All videos downloaded successfully! 🎉")
