import os
import subprocess
from datetime import datetime

def fetch_frame_from_live_stream(live_url, output_dir="frames"):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get current timestamp for unique filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = os.path.join(output_dir, f"frame_{timestamp}.jpeg")

    # Use ffmpeg to fetch a single frame
    ffmpeg_command = [
        "ffmpeg",
        "-i", live_url,         # Input live stream URL
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
    live_stream_url = os.getenv("YOUTUBE_URL", "https://www.youtube.com/watch?v=YOUR_LIVE_STREAM_ID")
    fetch_frame_from_live_stream(live_stream_url)
