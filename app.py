import logging
import os
import subprocess
import sys
from datetime import datetime
from yt_dlp import YoutubeDL
from PIL import Image

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])

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
        logging.info("Thumbnail saved to %s", thumbnail_path)
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

    def run_command(self, command):
        logging.debug("command: %s", " ".join(command))
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Command failed with return code {e.returncode}")
            print(f"Command output: {e.output}")
            print(f"Error output: {e.stderr}")
            # exit(e.returncode)

    def ffmpeg(self, args, output_path):
        cmd = ["ffmpeg"]
        cmd.extend(args)
        cmd.extend([
            "-loglevel", "error",       # less output messages
            "-hide_banner"])            # no info banner on start
        cmd.append(output_path)
        self.run_command(cmd)

    def fetch_frame_from_live_stream(self):
        """
         Fetch a single frame from the live stream and save it as a JPEG.
        """

        output_file = self.output_path()
        self.make_output_dir()

        # Use ffmpeg to fetch a single frame
        self.ffmpeg([
            "-i", self.get_live_stream_url(),   # Input live stream URL
            "-frames:v", "1",                   # Extract only one frame
            "-q:v", "2"],                       # Quality level
            output_file)                        # Output image file

        logging.info("Frame saved to %s", output_file)
        return output_file

    def create_day_timelapse(self):
        now = datetime.now()
        timelapse_path = os.path.join(self.output_dir(),
                                      f"{now:%Y-%m-%d}.mp4")
        if os.path.exists(timelapse_path):
            os.remove(timelapse_path)
        self.ffmpeg([
            "-framerate", "24",
            "-pattern_type", "glob",
            "-i", f"{self.output_dir()}/*.jpeg",
            "-c:v", "libx264",
            "-pix_fmt", "yuvj420p"],
            timelapse_path)
        logging.info("Timelapse saved to %s", timelapse_path)

    def sync_cloud(self):
        """
        Copy local frames to object storage bucket.
        :return:
        """
        gcs = "gs://fogcat-webcam/frames"
        self.run_command(["gsutil", "-m", "rsync", "-r", "/frames/", gcs])
        logging.info("Synced /frames/ to %s", gcs)

    def execute(self):
        frame = self.fetch_frame_from_live_stream()
        self.generate_thumbnail(frame)
        self.create_day_timelapse()
        self.sync_cloud()


if __name__ == "__main__":
    tr = TimelapseRecorder(output_dir="/frames",
                           youtube_url=os.getenv("YOUTUBE_URL"))
    tr.execute()
