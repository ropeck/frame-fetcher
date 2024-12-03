import os
import subprocess
from datetime import datetime
from yt_dlp import YoutubeDL

def get_live_stream_url(youtube_url):
    # Fetch the direct URL of the live stream using yt_dlp.
    ydl_opts = {"format": "best", "quiet": True}
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            return info_dict.get("url", None)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch live stream URL: {e}")

def fetch_frame_from_live_stream(youtube_url, output_dir="/frames"):
    # Fetch a single frame from the live stream and save it as a JPEG.

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get the live stream URL
    try:
        live_stream_url = get_live_stream_url(youtube_url)
    except RuntimeError as e:
        print(f"Error fetching live stream URL: {e}")
        return

    # Get current timestamp for unique filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = os.path.join(output_dir, f"frame_{timestamp}.jpeg")

    # Use ffmpeg to fetch a single frame
    ffmpeg_command = [
        "ffmpeg",
        "-i", live_stream_url,  # Input live stream URL
        "-frames:v", "1",       # Extract only one frame
        "-q:v", "2",            # Quality level
        output_file             # Output image file
    ]

    try:
        subprocess.run(ffmpeg_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Frame saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while fetching frame: {e.stderr.decode()}")

if __name__ == "__main__":
    youtube_live_url = os.getenv("YOUTUBE_URL", "https://www.youtube.com/watch?v=YOUR_LIVE_STREAM_ID")
    fetch_frame_from_live_stream(youtube_live_url)
