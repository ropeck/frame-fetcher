#!/bin/bash

PATH=$PATH:/usr/sbin:/usr/bin:/bin:/usr/local/bin
PATH=$PATH:/root/google-cloud-sdk/bin:/usr/sbin

# login to gcp and run the hourly image script

if [ -f "/app/service-account-key.json" ]; then
  gcloud auth activate-service-account --key-file=/app/service-account-key.json
fi

python3 /app/app.py
