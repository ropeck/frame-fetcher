# Phase 3: Web Service Integration

## Summary of Completed Work

### 1. Web Service Implementation
- Developed a Flask-based web service to serve timelapse-related content:
  - **Endpoints Added**:
    - `/frames/<year>/<month>/<day>`: Lists available hourly snapshots for the given date.
    - `/gif/<year>/<month>/<day>`: Serves a GIF timelapse for the given date.
    - `/timelapse/<year>/<month>/<day>`: Serves a video timelapse for the given date.
    - `/thumbnails/<year>/<month>/<day>`: Lists available thumbnails for the given date.

### 2. Kubernetes Integration
- Deployed the web service on Kubernetes as `timelapse-web`.
- Configured PersistentVolumeClaim (PVC) to share saved frames, videos, and thumbnails between the frame-fetcher and web service.

### 3. Ingress Configuration
- Updated Ingress to route paths for the web service:
  - `/frames`
  - `/gif`
  - `/timelapse`
  - `/thumbnails`
- Added HTTPS support with a Let's Encrypt certificate for secure access.

### 4. Verification and Stability
- Confirmed that all endpoints are functional and properly routed.
- Verified logs from the `timelapse-web` pod, the Ingress, and backend processes for stability.
- Resolved all 404 errors and ensured consistent path rewriting.

### 5. Front Page Updates
- Integrated links to the timelapse features on the weather app's front page (`weather.fogcat5.com`).

## Status
**Phase 3 is complete and stable.**
