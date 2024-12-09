# Use Python 3.10 slim as base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app


# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg
RUN apt-get install -y curl

# Downloading gcloud package
RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz

# Installing the package
RUN mkdir -p /usr/local/gcloud \
  && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
  && /usr/local/gcloud/google-cloud-sdk/install.sh

# Adding the package path to local
ENV PATH=$PATH:/usr/local/gcloud/google-cloud-sdk/bin

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy Python script and requirements
COPY *.py requirements.txt endpoint.sh ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default environment variable
# rio sands webcam
ENV YOUTUBE_URL="https://www.youtube.com/watch?v=hXtYKDio1rQ"

# Run the script
CMD ["bash", "/app/endpoint.sh"]
