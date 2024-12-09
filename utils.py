# utils.py
from pathlib import Path

def construct_daily_directory(base_dir, year, month, day):
    """Construct the daily directory path."""
    return Path(base_dir) / f"{year}/{month:02d}/{day:02d}"

def get_video_path(base_dir, year, month, day):
    """Construct the path for the timelapse video."""
    return construct_daily_directory(base_dir, year, month, day) / f"{year}-{month:02d}-{day:02d}.mp4"

def get_gif_path(base_dir, year, month, day):
    """Construct the path for the GIF."""
    return construct_daily_directory(base_dir, year, month, day) / f"{year}-{month:02d}-{day:02d}.gif"

def list_thumbnails(base_dir, year, month, day):
    """List all thumbnails for a given day."""
    thumbnail_dir = construct_daily_directory(base_dir, year, month, day) / "thumbnails"
    return [str(thumb) for thumb in thumbnail_dir.iterdir() if thumb.is_file()]
