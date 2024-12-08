import os
import subprocess
from datetime import datetime
from yt_dlp import YoutubeDL
from PIL import Image


class TimelapseRecorder:
    def __init__(self, output_dir=None, youtube_url=None):
        self.output_dir_prefix = output_dir
        self.youtube_url = youtube_url

    def output_dir(self, t=None):
        if t is None:
            t = datetime.now()
        return f"{self.output_dir_prefix}/{t:%Y}/{t:%m}/{t:%d}"

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
        img.thumbnail((200, 200), Image.Resampling.LANCZOS)
        base_name = os.path.basename(image_path)
        thumbnail_path = os.path.join(thumb_dir, base_name)
        img.save(thumbnail_path, "JPEG")
        print(f"Thumbnail saved to {thumbnail_path}")
        return thumbnail_path

    def get_live_stream_url(self):
        # Fetch the direct URL of the live stream using yt_dlp.
        ydl_opts = {"format": "best", "quiet": True}
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(self.youtube_url, download=False)
                return info_dict.get("url", None)
        except Exception as e:
            raise RuntimeError(f"Failed to fetch live stream URL: {e}")

    def fetch_frame_from_live_stream(self):
        """
         Fetch a single frame from the live stream and save it as a JPEG.
        """

        output_file = self.output_path()
        self.make_output_dir()

        # Use ffmpeg to fetch a single frame
        ffmpeg_command = [
            "ffmpeg",
            "-i", self.get_live_stream_url(),  # Input live stream URL
            "-frames:v", "1",       # Extract only one frame
            "-q:v", "2",            # Quality level
            output_file             # Output image file
        ]

        subprocess.run(ffmpeg_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Frame saved to {output_file}")
        return output_file

    def create_day_timelapse(self):
        now = datetime.now()
        timelapse_path = os.path.join(self.output_dir(),
                                      f"{now:%Y-%m-%d}.mp4")
        if os.path.exists(timelapse_path):
            os.remove(timelapse_path)
        ffmpeg_command = [
            "ffmpeg",
            "-framerate", "24",
            "-pattern_type", "glob",
            "-i", f"{self.output_dir()}/*.jpeg",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            timelapse_path
        ]
        subprocess.run(ffmpeg_command, check=True)
        print(f"Timelapse saved to {timelapse_path}")

    def sync_cloud(self):
        """
        Copy local frames to object storage bucket.
        :return:
        """
        gcs = "gs://fogcat-webcam/frames"
        result = subprocess.run(["gsutil", "-m", "rsync", "-r",
                                 "/frames/", gcs],
                                 capture_output=True)
        if result.returncode == 0:
            print(f"Synced /frames/ to {gcs}")
        else:
            print(f"Failed to sync: {result.stderr.decode()}")

    def execute(self):
        frame = self.fetch_frame_from_live_stream()
        self.generate_thumbnail(frame)
        self.create_day_timelapse()
        self.sync_cloud()


if __name__ == "__main__":
    tr = TimelapseRecorder(output_dir="/frames",
                           youtube_url=os.getenv("YOUTUBE_URL"))
    tr.execute()
