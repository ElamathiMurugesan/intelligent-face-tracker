# AI-Driven Unique Visitor Counter

## 1. Project Overview

This project is an AI-driven unique visitor counter that detects, tracks, recognizes, and registers faces from a video stream.

The system automatically assigns a persistent visitor ID to a new person and recognizes the same visitor when they appear again.

The system records:

- Unique visitor count
- Visitor entry
- Visitor exit
- Timestamp
- Face image
- Visitor identity
- Tracking ID
- Recognition similarity
- System events

The development version uses a sample video file. The video source can also be configured for an RTSP camera stream.

---

## 2. Problem Statement

Traditional visitor counting systems may count the same person multiple times when the person appears in different frames.

This project addresses the problem by combining:

- AI face detection
- Face recognition
- Object tracking
- Persistent visitor identification
- Database storage
- Entry and exit event management

The goal is to count unique people rather than simply counting detected faces.

---

## 3. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.11 |
| Face Detection | YOLOv11 Face |
| Face Recognition | InsightFace / ArcFace |
| Face Embedding | 512-dimensional embedding |
| Tracking | ByteTrack |
| Video Processing | OpenCV |
| Database | SQLite |
| Configuration | JSON |
| Logging | Local log file |
| Image Storage | Local filesystem |

---

## 4. System Architecture

The system follows this processing pipeline:

```text
Video / RTSP Camera
        |
        v
OpenCV Frame Capture
        |
        v
YOLO Face Detection
        |
        v
ByteTrack Tracking
        |
        v
Face Crop
        |
        v
InsightFace / ArcFace
        |
        v
512-D Face Embedding
        |
        v
Cosine Similarity Matching
        |
        +----------------------+
        |                      |
        v                      v
Existing Visitor        New Visitor
        |                      |
        v                      v
Recognition             Registration
        |                      |
        +----------+-----------+
                   |
                   v
             Entry / Exit
             Event Manager
                   |
       +-----------+-----------+
       |           |           |
       v           v           v
    SQLite      Images     events.log
       |
       v
Unique Visitor Count
```

### Processing Flow

1. OpenCV reads frames from the video or camera stream.
2. YOLOv11 Face detects faces in the frame.
3. ByteTrack assigns tracking IDs to detected faces.
4. The face region is passed to InsightFace.
5. InsightFace generates a 512-dimensional face embedding.
6. The embedding is compared with stored visitor embeddings using cosine similarity.
7. If the similarity is above the configured threshold, the visitor is recognized.
8. If no suitable match exists, a new visitor ID is registered.
9. Entry and exit events are recorded.
10. Face images, database records, and system logs are stored locally.
11. The application displays the unique visitor count.

---

## 5. Key Features

- Real-time face detection using YOLOv11 Face
- Face tracking using ByteTrack
- Face recognition using InsightFace / ArcFace
- 512-dimensional face embeddings
- Persistent visitor identification using SQLite
- Automatic registration of new visitors
- Recognition of previously registered visitors
- Unique visitor counting
- Entry event detection
- Exit event detection using tracking timeout
- Timestamped visitor entry and exit records
- Face image storage for entry and exit events
- Tracking ID associated with each detected face
- Recognition similarity score logging
- Centralized event logging using `events.log`
- JSON-based configuration
- Video file input
- Configurable RTSP camera input
- Modular Python implementation

---

## 6. Project Structure

```text
intelligent-face-tracker/
│
├── app.py
├── config.json
├── requirements.txt
├── README.md
│
├── database.py
├── visitor_manager.py
├── event_manager.py
│
├── yolov11n-face.pt
├── sample.mp4
│
├── data/
│   └── visitors.db
│
├── logs/
│   ├── events.log
│   ├── entries/
│   └── exits/
│
└── docs/
    └── planning.md
```

### File Description

| File / Folder | Purpose |
|---|---|
| `app.py` | Main application for detection, tracking, recognition, and visitor processing |
| `config.json` | Stores configurable application parameters |
| `requirements.txt` | Lists Python dependencies |
| `README.md` | Project documentation |
| `database.py` | Creates and manages the SQLite database |
| `visitor_manager.py` | Performs visitor matching, identification, and registration |
| `event_manager.py` | Handles entry, exit, image storage, and event logging |
| `yolov11n-face.pt` | YOLOv11 face detection model |
| `sample.mp4` | Development/test video |
| `data/visitors.db` | Persistent visitor database |
| `logs/events.log` | System event log |
| `logs/entries/` | Stores visitor entry images |
| `logs/exits/` | Stores visitor exit images |
| `docs/planning.md` | AI planning and development approach |

---

## 7. Installation and Setup

### 7.1 Requirements

The project requires:

- Python 3.11
- pip
- Virtual environment
- OpenCV
- Ultralytics YOLO
- InsightFace
- NumPy
- PyTorch
- TorchVision
- ByteTrack dependencies
- SQLite

### 7.2 Create Virtual Environment

Open PowerShell in the project directory:

```powershell
python -m venv venv
```

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

### 7.3 Install Dependencies

Install the required Python packages:

```powershell
pip install -r requirements.txt
```

### 7.4 Verify Python

```powershell
python --version
```

Expected environment:

```text
Python 3.11.x
```

---

## 8. Configuration

The project uses `config.json` for configurable parameters.

Example:

```json
{
  "video_source": "sample.mp4",
  "detection_skip_frames": 5,
  "face_match_threshold": 0.5,
  "exit_timeout_seconds": 2,
  "database_path": "data/visitors.db",
  "entry_log_directory": "logs/entries",
  "exit_log_directory": "logs/exits",
  "event_log": "logs/events.log"
}
```

### Configuration Parameters

| Parameter | Description |
|---|---|
| `video_source` | Video file or camera source |
| `detection_skip_frames` | Configuration value for controlling detection frequency |
| `face_match_threshold` | Minimum cosine similarity used for visitor matching |
| `exit_timeout_seconds` | Time used to determine when a tracked visitor has exited |
| `database_path` | Location of SQLite database |
| `entry_log_directory` | Directory for entry images |
| `exit_log_directory` | Directory for exit images |
| `event_log` | Location of the central event log |

### Face Match Threshold

The current development configuration uses:

```text
0.5
```

The threshold determines whether an embedding is considered similar enough to an existing visitor.

A higher threshold makes matching stricter, while a lower threshold allows more matches.

The threshold should be validated further with a larger real-world dataset before production deployment.

---

## 9. Running the Application

Make sure the virtual environment is activated:

```powershell
.\venv\Scripts\Activate.ps1
```

Run:

```powershell
python app.py
```

The application will:

1. Load the YOLO face detector.
2. Load InsightFace.
3. Load existing visitors from SQLite.
4. Open the configured video source.
5. Detect faces.
6. Track faces using ByteTrack.
7. Generate face embeddings.
8. Compare embeddings with stored visitors.
9. Register new visitors when required.
10. Record entry events.
11. Monitor tracked visitors.
12. Record exit events.
13. Display the unique visitor count.

---

## 10. Face Recognition Process

The face recognition pipeline consists of three major steps.

### Step 1: Face Detection

YOLOv11 Face detects the location of faces in the frame.

```text
Input Frame
     |
     v
YOLOv11 Face
     |
     v
Face Bounding Box
```

### Step 2: Face Embedding

The detected face is processed by InsightFace / ArcFace.

The model generates a:

```text
512-dimensional face embedding
```

The embedding represents facial features numerically.

### Step 3: Similarity Matching

The generated embedding is compared with previously stored embeddings using cosine similarity.

```text
New Face
   |
   v
512-D Embedding
   |
   v
Compare with Database
   |
   +----------------------+
   |                      |
Similarity >= Threshold   Similarity < Threshold
   |                      |
   v                      v
Existing Visitor        New Visitor
```

---

## 11. Visitor Registration

When a face is detected for the first time and no stored embedding meets the configured similarity threshold, the system creates a new visitor ID.

Example:

```text
V001
V002
V003
V004
...
```

The visitor embedding and timestamps are stored in SQLite.

Example database record:

```text
Visitor ID: V001
First Seen: 2026-10-03 17:58:49
Last Seen: 2026-10-03 ...
Embedding: 512-dimensional vector
```

The visitor ID remains persistent across application runs as long as the SQLite database is retained.

---

## 12. Visitor Recognition

When a previously registered person appears again, the newly generated embedding is compared with stored embeddings.

Example:

```text
Detected Face
     |
     v
Embedding
     |
     v
Database Matching
     |
     v
V001
Similarity: 0.72
```

The system can then associate the current tracking ID with the persistent visitor ID.

### Important Difference

The system uses two different identifiers:

**Tracking ID**

Identifies a face during the current video tracking session.

**Visitor ID**

Identifies the persistent person stored in the database.

Example:

```text
Track ID 137  --->  Visitor V001
Track ID 59   --->  Visitor V002
```

A tracking ID can change between different appearances, while the persistent visitor ID is intended to remain associated with the recognized person.

---

## 13. Entry Event Management

An entry event is generated when a visitor is identified and becomes active in the current session.

The system stores:

- Visitor ID
- Tracking ID
- Timestamp
- Entry image
- Event type

Example:

```text
ENTRY | Visitor: V001 | Track: 137
```

Entry images are stored inside:

```text
logs/entries/
```

Example:

```text
logs/entries/V001_20261003_175849.jpg
```

---

## 14. Exit Event Management

The system monitors active tracking IDs.

If a tracked visitor is no longer detected for the configured timeout period, the system treats the visitor as having exited.

Current configuration:

```json
"exit_timeout_seconds": 2
```

Example:

```text
EXIT | Visitor: V004 | Track: 281
```

Exit images are stored inside:

```text
logs/exits/
```

Example:

```text
logs/exits/V004_20261003_180735.jpg
```

This prevents an exit event from being generated for every frame.

---

## 15. Unique Visitor Counting

The system maintains a persistent visitor identity instead of simply counting face detections.

For example:

```text
Frame 1:
Person A detected

Frame 2:
Person A detected

Frame 3:
Person A detected

Frame 4:
Person A detected
```

The system does not count this as four visitors.

It identifies the person as:

```text
Visitor V001
```

Therefore:

```text
Unique Visitors = 1
```

If another person appears:

```text
Visitor V002
```

then:

```text
Unique Visitors = 2
```

---

## 16. Database

SQLite is used for persistent storage.

The database is located at:

```text
data/visitors.db
```

### Visitors Table

The visitors table stores persistent visitor information.

```text
visitors
---------------------------------------
visitor_id
embedding
first_seen
last_seen
```

### Events Table

The events table stores system events.

```text
events
---------------------------------------
id
visitor_id
event_type
timestamp
```

### Example Events

```text
V001 | ENTRY | 2026-10-03 ...
V002 | ENTRY | 2026-10-03 ...
V004 | EXIT  | 2026-10-03 ...
V003 | EXIT  | 2026-10-03 ...
```

---

## 17. Event Logging

The system maintains a central event log:

```text
logs/events.log
```

The log records important processing events such as:

- Embedding generation
- Tracking started
- Visitor registration
- Recognition
- Entry
- Exit

Example:

```text
2026-10-03 17:58:48 | EMBEDDING_GENERATED | Visitor: UNKNOWN | Track: 137

2026-10-03 17:58:48 | TRACKING_STARTED | Visitor: V001 | Track: 137

2026-10-03 17:58:49 | REGISTRATION | Visitor: V001 | Track: 137

2026-10-03 17:58:49 | ENTRY | Visitor: V001 | Track: 137 | Image: logs/entries\V001_20261003_175849.jpg
```

Exit example:

```text
2026-10-03 18:07:35 | EXIT | Visitor: V004 | Track: 281 | Image: logs/exits\V004_20261003_180735.jpg
```

---

## 18. Sample Development Output

The development video was processed successfully with:

```text
Total Frames: 240
Unique Visitors: 6
```

The system registered six visitors during the clean development run:

```text
V001
V002
V003
V004
V005
V006
```

Example entry events:

```text
ENTRY | Visitor: V001 | Track: 137
ENTRY | Visitor: V002 | Track: 59
ENTRY | Visitor: V003 | Track: 153
ENTRY | Visitor: V004 | Track: 281
ENTRY | Visitor: V005 | Track: 391
ENTRY | Visitor: V006 | Track: 247
```

Example exit event:

```text
EXIT | Visitor: V004 | Track: 281
```

At the end of the video, remaining active visitors were also processed as exits.

Final output:

```text
Recognition completed!
Unique visitors: 6
```

---

## 19. Sample Output Files

After running the application, the project generates files such as:

```text
logs/
│
├── events.log
│
├── entries/
│   ├── V001_20261003_175849.jpg
│   ├── V002_20261003_180120.jpg
│   ├── V003_20261003_180211.jpg
│   ├── V004_20261003_180451.jpg
│   ├── V005_20261003_180621.jpg
│   └── V006_20261003_181046.jpg
│
└── exits/
    ├── V001_20261003_181056.jpg
    ├── V002_20261003_181056.jpg
    ├── V003_20261003_181056.jpg
    ├── V004_20261003_180735.jpg
    ├── V005_20261003_181056.jpg
    └── V006_20261003_181056.jpg
```

The SQLite database is stored at:

```text
data/visitors.db
```

---

## 20. Performance and Compute Load

The application was tested using the development video containing 240 frames.

During the latest development run, the YOLO processing output reported approximately:

```text
Preprocess: 2.9 ms/image
Inference: 34.8 ms/image
Postprocess: 1.1 ms/image
```

The actual processing time can vary depending on:

- CPU/GPU hardware
- Video resolution
- Number of faces in a frame
- YOLO model size
- InsightFace processing
- Number of stored visitors
- Tracking complexity

The application uses lightweight YOLO face detection together with InsightFace recognition and ByteTrack tracking.

For production deployment, GPU acceleration can be considered to improve throughput for higher-resolution or multi-camera streams.

---

## 21. Detection Frequency Configuration

The configuration contains:

```json
"detection_skip_frames": 5
```

This parameter is intended to control detection frequency as an optimization setting.

The current development implementation prioritizes continuous YOLO tracking across the video frames for tracking stability. Therefore, the configuration value is loaded and displayed, but the current test implementation does not claim that YOLO detection is skipped on every fifth frame.

Future optimization can use frame skipping together with an appropriate tracking/prediction strategy.

---

## 22. RTSP Camera Support

The development version uses:

```text
sample.mp4
```

The video source is configurable through:

```json
"video_source"
```

For a live camera deployment, the value can be changed to an RTSP stream.

Example:

```json
{
  "video_source": "rtsp://camera-address/stream"
}
```

The application architecture remains:

```text
RTSP Camera
     |
     v
OpenCV
     |
     v
YOLO Face Detection
     |
     v
ByteTrack
     |
     v
InsightFace
     |
     v
SQLite + Logs + Images
```

The RTSP configuration is part of the deployment design; the development validation was performed using the supplied sample video.

---

## 23. Entry and Exit Exactly Once

The application uses active visitor state and tracking information to avoid generating an entry event for every frame.

For example:

```text
Frame 1  -> V001 detected -> ENTRY
Frame 2  -> V001 detected -> no new ENTRY
Frame 3  -> V001 detected -> no new ENTRY
Frame 4  -> V001 detected -> no new ENTRY
```

When the visitor disappears for the configured timeout:

```text
Visitor V001 -> EXIT
```

This provides session-level entry and exit event handling instead of frame-level counting.

---

## 24. Persistent Visitor Identity

The SQLite database stores visitor embeddings so that visitor information is retained after the current processing session.

Example:

### First appearance

```text
Person A
   |
   v
No matching embedding
   |
   v
Register V001
```

### Later appearance

```text
Person A
   |
   v
Generate embedding
   |
   v
Compare with database
   |
   v
Match V001
```

Therefore, the system can distinguish:

```text
Person A -> V001
Person B -> V002
Person C -> V003
```

instead of creating a new visitor ID every time a person appears.

---

## 25. AI Planning and Development Approach

The project was developed using an AI-assisted development workflow.

The development process was divided into smaller modules:

1. Environment setup
2. YOLO face detection testing
3. InsightFace face detection testing
4. Face embedding generation
5. SQLite database creation
6. Visitor registration
7. Cosine similarity matching
8. ByteTrack integration
9. Face recognition integration
10. Entry event management
11. Exit event management
12. Event logging
13. Configuration integration
14. End-to-end testing
15. README and documentation

AI assistance was used for:

- Project architecture planning
- Python module development
- Debugging
- Test scripts
- Database design
- Recognition logic
- Logging logic
- Documentation
- Error analysis

The implementation was tested incrementally after each major component.

The detailed planning document is available at:

```text
docs/planning.md
```

---

## 26. Assumptions

The project uses the following assumptions:

- The input stream contains visible human faces.
- The face detection model can detect the required faces.
- The face crop is sufficiently clear for recognition.
- The stored embedding represents the visitor adequately.
- The similarity threshold is configurable.
- A visitor is considered to have exited after being absent for the configured timeout.
- SQLite is sufficient for the development and demonstration environment.
- The local filesystem is available for storing event images and logs.

---

## 27. Limitations

The current development implementation has the following limitations:

- Recognition performance depends on lighting, face angle, image quality, occlusion, and camera position.
- Similarity threshold requires further validation with a larger dataset.
- The development validation uses the supplied sample video.
- RTSP camera input is configurable but was not validated using a live RTSP camera during development.
- The current implementation uses SQLite and local filesystem storage rather than a distributed database or cloud storage.
- Detection skipping is currently represented as a configuration parameter but is not actively applied to the YOLO tracking loop.
- Large-scale multi-camera deployment would require additional optimization and centralized storage.
- Face recognition accuracy should be evaluated with a representative real-world dataset before production deployment.

---

## 28. Security and Privacy Considerations

The application processes facial information and therefore requires appropriate handling of biometric data.

The development system stores:

- Face embeddings
- Visitor IDs
- Entry images
- Exit images
- Timestamps

For production deployment, appropriate access control, data retention, encryption, consent requirements, and applicable privacy regulations should be considered.

---

## 29. Testing Performed

The following components were tested individually and together:

| Test | Result |
|---|---|
| Python virtual environment | Passed |
| YOLO model loading | Passed |
| YOLO face detection | Passed |
| InsightFace loading | Passed |
| Face detection with InsightFace | Passed |
| 512-D embedding generation | Passed |
| SQLite database creation | Passed |
| Visitor registration | Passed |
| Cosine similarity matching | Passed |
| ByteTrack integration | Passed |
| Face tracking + embedding | Passed |
| Recognition pipeline | Passed |
| Entry event creation | Passed |
| Exit event creation | Passed |
| Image storage | Passed |
| Event logging | Passed |
| End-to-end video processing | Passed |
| 240-frame development video | Passed |

---

## 30. Final Development Test

The final development test successfully processed the complete sample video.

Example output:

```text
Loading YOLO face detector...
Loading InsightFace...
Models loaded successfully.

Existing visitors: 6

Video FPS: 29.97002997002997

Exit timeout: 2 seconds
Exit timeout frames: 59
Detection skip frames: 5

...

Recognition completed!
Unique visitors: 6
```

The development run completed all 240 frames without an application crash.

---

## 31. Demo Video

Demo video:

```text
https://youtu.be/zhyBbHIf3Co
```

The demo should show:

1. Application startup
2. Face detection
3. Tracking IDs
4. Visitor IDs
5. Recognition
6. New visitor registration
7. Unique visitor count
8. Entry image generation
9. Exit event
10. `events.log`
11. SQLite database
12. Stored entry and exit images

---

## 32. Architecture Diagram

The architecture diagram for the project will be stored at:

```text
docs/architecture.png
```

The diagram represents:

```text
Video / RTSP
     |
     v
OpenCV
     |
     v
YOLO Face Detection
     |
     v
ByteTrack
     |
     v
InsightFace / ArcFace
     |
     v
512-D Embedding
     |
     v
Cosine Similarity
     |
     +------------------+
     |                  |
     v                  v
Existing Visitor    New Visitor
     |                  |
     v                  v
Recognition        Registration
     |                  |
     +--------+---------+
              |
              v
       Entry / Exit
              |
       +------+------+ 
       |      |      |
       v      v      v
    SQLite  Images  events.log
              |
              v
      Unique Visitor Count
```

---

## 33. Future Improvements

Possible future improvements include:

- Improved face recognition threshold calibration
- GPU acceleration
- Advanced multi-camera support
- Centralized database
- Cloud storage
- Web dashboard
- Visitor analytics
- Daily and monthly visitor reports
- Better re-identification across cameras
- More robust occlusion handling
- Improved frame-skipping and tracking optimization
- Authentication and role-based access
- Data encryption
- Configurable retention policies

---

## 34. Conclusion

The AI-Driven Unique Visitor Counter combines face detection, face recognition, tracking, persistent identity management, database storage, and event logging into a single pipeline.

The system is designed to count unique visitors rather than counting every face detection.

The development implementation successfully demonstrates:

- Face detection
- Face tracking
- Face embedding generation
- Visitor registration
- Visitor recognition
- Unique visitor counting
- Entry event recording
- Exit event recording
- Timestamped image storage
- SQLite persistence
- Centralized event logging

The architecture can be extended from a development video source to a live RTSP camera deployment.

---

## 35. Hackathon

This project is a part of a hackathon run by https://katomaran.com
