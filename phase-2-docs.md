
# Phase 2: Thumbnail Generation, Timelapse Updates, and GCS Sync

## **Overview**
Phase 2 focuses on enhancing the `frame-fetcher` project by implementing the following key features:
- Generating thumbnails for each frame as it is captured.
- Dynamically updating the timelapse video for the current day.
- Syncing frames, thumbnails, and timelapse videos to a Google Cloud Storage (GCS) bucket for backup and accessibility.

---

## **Features Implemented**

### **1. Thumbnail Generation**
- For each frame saved, a corresponding thumbnail is generated with a maximum size of `200x200` pixels.
- Thumbnails are stored in a `thumbnails` subdirectory within the daily directory structure:
  ```
  /frames/YYYY/MM/DD/thumbnails/
  ```
- **Tool Used**: The Python Pillow library (`PIL.Image`) for high-quality resizing.

---

### **2. Dynamic Timelapse Updates**
- A timelapse video (`timelapse.mp4`) is created or updated dynamically for the current day.
- The timelapse includes all frames in the daily directory.
- **Tool Used**: `ffmpeg` for efficient video generation.

File structure:
```
/frames/YYYY/MM/DD/timelapse.mp4
```

---

### **3. Google Cloud Storage Sync**
- All captured frames, thumbnails, and timelapse videos are synced to a designated GCS bucket.
- **Tool Used**: `gsutil` and the Google Cloud Python SDK for seamless integration.

---

## **Workflow**
1. **Frame Capture**:
   - Frames are saved to daily directories in `/frames/YYYY/MM/DD/`.

2. **Thumbnail Generation**:
   - Each frame generates a corresponding thumbnail, saved in the `thumbnails` subdirectory.

3. **Timelapse Updates**:
   - A new frame triggers the update of the day’s timelapse video.

4. **Cloud Backup**:
   - The entire daily directory (frames, thumbnails, timelapse) is synced to the GCS bucket.

---

## **Deployment Instructions**

### **1. Build and Deploy the Docker Image**
Build the updated Docker image:
```bash
docker build -t frame-fetcher:0.1.1 .
docker tag frame-fetcher:0.1.1 <your-registry>/frame-fetcher:0.1.1
docker push <your-registry>/frame-fetcher:0.1.1
```

Update the CronJob on Kubernetes:
1. Edit the CronJob to use the new image:
   ```yaml
   image: <your-registry>/frame-fetcher:0.1.1
   imagePullPolicy: Always
   ```

2. Apply the updated CronJob:
   ```bash
   kubectl apply -f frame-fetcher-cronjob.yaml
   ```

---

## **Validation Results**
The following tests were performed to confirm the successful implementation of Phase 2:
1. **Thumbnail Generation**:
   - Verified thumbnails are generated for each frame.
   - Confirmed thumbnail quality and file size.

2. **Timelapse Updates**:
   - Successfully generated timelapse videos.
   - Confirmed videos dynamically update as new frames are added.

3. **GCS Sync**:
   - Verified all files (frames, thumbnails, timelapse videos) are synced to the GCS bucket with the correct directory structure.
   - Confirmed local and cloud directories match after syncing.

---

## **File Structure**
Example directory structure after Phase 2:
```
/frames/
└── 2024/
    └── 12/
        └── 07/
            ├── 08-00-00.jpeg
            ├── 08-00-00-thumb.jpeg
            ├── thumbnails/
            │   ├── thumb_08-00-00.jpeg
            ├── timelapse.mp4
```

---

## **Next Steps**
Phase 3 will focus on:
- Building a web server to view and select timelapse videos.
- Integrating the web server as a subdirectory under `weather.fogcat5.com`.
- Adding links for the timelapse cam to the main **fogcat5.com** page.

---

## **Acknowledgments**
This phase was completed with significant testing locally and in the GKE cluster to ensure reliability and scalability.
