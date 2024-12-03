# Use Python 3.10 slim as base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy Python script and requirements
COPY app.py requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Default environment variable
# rio sands webcam
ENV YOUTUBE_URL="https://www.youtube.com/watch?v=hXtYKDio1rQ"

# Run the script
CMD ["python", "app.py"]
