import os
import subprocess
from datetime import datetime
from yt_dlp import YoutubeDL
from PIL import Image



def get_live_stream_url(youtube_url):
    # Fetch the direct URL of the live stream using yt_dlp.
    ydl_opts = {"format": "best", "quiet": True}
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            return info_dict.get("url", None)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch live stream URL: {e}")

class TimelapseRecorder:
    def __init__(self, output_dir=None):
        self.output_dir = output_dir

    def output_dir(self, t):
        if t is None:
            t = datetime.now()
        return f"/{self.output_dir}/{t:%Y}/{t:%m}/{t:%d}"
    def make_output_dir(self, timestamp=None):
        os.makedirs(self.output_dir(timestamp), exist_ok=True)
    def output_path(self, timestamp=None):
        if timestamp is None:
            timestamp = datetime.now()
        file_name = f"{timestamp:%Y-%m-%d-%H-%M-%S}.jpeg"
        return os.path.join(self.output_dir(), file_name)

    def generate_thumbnail(self, image_path):
        dir = os.path.dirname(image_path)
        thumb_dir = os.path.join(dir, "thumbnails")
        os.makedirs(thumb_dir, exist_ok=True)
        img = Image.open(image_path)
        img.thumbnail((200, 200), Image.ANTIALIAS)
        base_name = os.path.basename(image_path)
        thumbnail_path = os.path.join(thumb_dir, base_name)
        img.save(thumbnail_path, "JPEG")
        print(f"Thumbnail saved to {thumbnail_path}")
        return thumbnail_path

    def fetch_frame_from_live_stream(youtube_url):
        """
         Fetch a single frame from the live stream and save it as a JPEG.

        :param youtube_url: youtube video url to sample and save to output_dir
        """

        output_file = self.output_path()
        self.make_output_dir()

        # Get the live stream URL
        try:
            live_stream_url = get_live_stream_url(youtube_url)
        except RuntimeError as e:
            print(f"Error fetching live stream URL: {e}")
            return

        # Use ffmpeg to fetch a single frame
        ffmpeg_command = [
            "ffmpeg",
            "-i", live_stream_url,  # Input live stream URL
            "-frames:v", "1",       # Extract only one frame
            "-q:v", "2",            # Quality level
            output_file             # Output image file
        ]

        subprocess.run(ffmpeg_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Frame saved to {output_file}")
        return output_file

if __name__ == "__main__":
    tr = TimelapseRecorder("/frames")
    youtube_live_url = os.getenv("YOUTUBE_URL", "https://www.youtube.com/watch?v=YOUR_LIVE_STREAM_ID")
    frame = tr.fetch_frame_from_live_stream(youtube_live_url)
    tr.generate_thumbnail(frame)
