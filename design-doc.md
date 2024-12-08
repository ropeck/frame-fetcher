# Frame-Fetcher Timelapse Processing Deployment

This document outlines the planned goals and phases for enhancing the **frame-fetcher** Kubernetes deployment. The deployment currently captures a frame once an hour and saves it to a PVC (`/frames`). The following phases describe incremental improvements to the system.

---

## **Planned Phases**

### **Phase 1: Timelapse Video Creation**
- Group the hourly images by day.
- Process the images to create a timelapse video for each day.
- Ensure timelapse videos are stored in an organized structure for easy access.

### **Phase 2: App Enhancements and Cloud Sync**
- **Directory Organization**: Update the `app.py` script run by the CronJob to:
  - Save new frames into directories organized by date (`YYYY-MM-DD`).
- **Thumbnails**: Generate a thumbnail for each frame upon saving.
- **Dynamic Timelapse Updates**: Update the current day's timelapse dynamically as new frames are captured.
- **Cloud Backup**:
  - Sync saved images and timelapse videos to a Google Cloud Storage (GCS) bucket.
  - Implement checks to ensure the local and cloud copies are consistent.

### **Phase 3: Web Server for Timelapse Viewing**
- Build a web server to:
  - Display and allow selection of daily timelapse videos.
  - Provide an intuitive interface for users to view the captured timelapses.
- Integrate the web server with the existing `weather.fogcat5.com` site:
  - Add the timelapse viewer as a subdirectory (e.g., `weather.fogcat5.com/timelapse`).
  - Update the **fogcat5.com** front page to include links to the timelapse viewer.

### **Phase 4: Cloud Integration and Event-Driven Processing**
- Add cloud-native enhancements to streamline and scale the processing:
  - Implement Pub/Sub listeners to trigger further processing or notifications when new images are saved.
  - Leverage additional GCP tools (e.g., Cloud Functions or Workflows) for automated pipeline improvements.
- Expand support for real-time or near-real-time processing for use cases like live timelapse previews.

---

## **Next Steps**
1. Begin Phase 1 by analyzing the current `/frames` directory and identifying the grouping and processing logic for daily timelapses.
2. Gradually implement subsequent phases, ensuring incremental validation and testing at each step.
3. Document all changes in the repository and update this plan as needed.

---