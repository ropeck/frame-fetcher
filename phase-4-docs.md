# Phase 4: Frontend UI for Timelapse Browsing

## Goals
- Create a user-friendly web interface to browse timelapse videos, GIFs, and hourly snapshots.
- Add a page at `/timelapse` on `weather.fogcat5.com` for the frontend UI.
- Provide navigation for:
  - Viewing available timelapse videos (one per day).
  - Accessing GIF timelapses for specific days.
  - Browsing hourly snapshots by date and time.

## Deliverables
- **UI Design**:
  - Clean and responsive design for browsing timelapse content.
- **Integration with Backend**:
  - Use the existing API endpoints (`/frames`, `/gif`, `/timelapse`, `/thumbnails`) to fetch data dynamically.
- **Deployment**:
  - Integrate the new UI with the existing Flask web service (`timelapse-web`).
  - Ensure the UI is accessible via `/timelapse`.

---

# Phase 5: Cloud Integration and Real-Time Updates

## Goals
- Implement real-time updates for frames using Google Cloud Pub/Sub.
- Automatically trigger processing for new frames as they are added.
- Sync processed frames, videos, and GIFs to Google Cloud Storage (GCS) more efficiently.

## Deliverables
- **Pub/Sub Integration**:
  - Set up a Pub/Sub topic and subscription for frame updates.
  - Configure the backend to listen for new frames and trigger processing jobs.
- **Real-Time Processing**:
  - Enhance the frame-fetcher to process frames immediately as they are received.
- **Metrics and Monitoring**:
  - Add Prometheus metrics for processing performance and storage usage.
