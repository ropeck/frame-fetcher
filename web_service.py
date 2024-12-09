from flask import Flask, send_file, jsonify
from utils import get_video_path, get_gif_path, list_thumbnails, construct_daily_directory

app = Flask(__name__)
BASE_DIR = "/frames"

@app.route("/frames/<int:year>/<int:month>/<int:day>")
def list_frames(year, month, day):
    """List all full-sized frames for the given day."""
    try:
        frame_dir = construct_daily_directory(BASE_DIR, year, month, day)
        frames = [f"/frames/{year}/{month}/{day}/{frame.name}" for frame in frame_dir.iterdir() if frame.is_file()]
        return jsonify({"frames": frames})
    except FileNotFoundError:
        return jsonify({"error": "No frames found for the given date"}), 404

@app.route("/frames/<int:year>/<int:month>/<int:day>/<frame_name>")
def serve_frame(year, month, day, frame_name):
    """Serve a specific full-sized frame."""
    frame_path = construct_daily_directory(BASE_DIR, year, month, day) / frame_name
    if not frame_path.exists():
        return jsonify({"error": "Frame not found"}), 404
    return send_file(frame_path, mimetype="image/jpeg")

@app.route("/thumbnails/<int:year>/<int:month>/<int:day>")
def list_thumbnails_endpoint(year, month, day):
    """List all thumbnails for the given day."""
    try:
        thumbnails = list_thumbnails(BASE_DIR, year, month, day)
        return jsonify({"thumbnails": thumbnails})
    except FileNotFoundError:
        return jsonify({"error": "No thumbnails found for the given date"}), 404

@app.route("/thumbnails/<int:year>/<int:month>/<int:day>/<thumbnail_name>")
def serve_thumbnail(year, month, day, thumbnail_name):
    """Serve a specific thumbnail."""
    thumb_dir = construct_daily_directory(BASE_DIR, year, month, day) / "thumbnails"
    thumbnail_path = thumb_dir / thumbnail_name
    if not thumbnail_path.exists():
        return jsonify({"error": "Thumbnail not found"}), 404
    return send_file(thumbnail_path, mimetype="image/jpeg")

@app.route("/timelapse/<int:year>/<int:month>/<int:day>.mp4")
def serve_timelapse(year, month, day):
    video_path = get_video_path(BASE_DIR, year, month, day)
    if not video_path.exists():
        return jsonify({"error": "Timelapse not found"}), 404
    return send_file(video_path, mimetype="video/mp4")

@app.route("/gif/<int:year>/<int:month>/<int:day>.gif")
def serve_gif(year, month, day):
    gif_path = get_gif_path(BASE_DIR, year, month, day)
    if not gif_path.exists():
        return jsonify({"error": "GIF not found"}), 404
    return send_file(gif_path, mimetype="image/gif")

@app.route('/healthz')
def healthz():
    return jsonify({"status": "ok"}), 200
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
