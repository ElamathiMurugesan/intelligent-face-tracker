import cv2
import json
from ultralytics import YOLO
from insightface.app import FaceAnalysis

from database import create_database
from visitor_manager import load_visitors, identify_visitor
from event_manager import (
    create_entry_event,
    create_exit_event,
    write_event_log
)


# ==========================================
# LOAD CONFIGURATION
# ==========================================

with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)


VIDEO_SOURCE = config["video_source"]
DETECTION_SKIP_FRAMES = config["detection_skip_frames"]

EXIT_TIMEOUT_SECONDS = config["exit_timeout_seconds"]

# Video FPS will be used to convert seconds to frames
# Default value until the video is opened
EXIT_TIMEOUT_FRAMES = 30


# ==========================================
# LOAD MODELS
# ==========================================

YOLO_MODEL = "yolov11n-face.pt"

print("Loading YOLO face detector...")

model = YOLO(YOLO_MODEL)

print("Loading InsightFace...")

face_app = FaceAnalysis(name="buffalo_l")

face_app.prepare(
    ctx_id=0,
    det_size=(640, 640)
)

print("Models loaded successfully.")


# ==========================================
# DATABASE
# ==========================================

create_database()

visitors = load_visitors()

print(
    "Existing visitors:",
    len(visitors)
)


# ==========================================
# OPEN VIDEO
# ==========================================

cap = cv2.VideoCapture(VIDEO_SOURCE)

if not cap.isOpened():
    print(
        "ERROR: Could not open video source:",
        VIDEO_SOURCE
    )
    exit()


fps = cap.get(cv2.CAP_PROP_FPS)

if fps <= 0:
    fps = 15


EXIT_TIMEOUT_FRAMES = int(
    EXIT_TIMEOUT_SECONDS * fps
)

print(
    "Video FPS:",
    fps
)

print(
    "Exit timeout:",
    EXIT_TIMEOUT_SECONDS,
    "seconds"
)

print(
    "Exit timeout frames:",
    EXIT_TIMEOUT_FRAMES
)
print("Detection skip frames:", DETECTION_SKIP_FRAMES)


cap.release()


# ==========================================
# TRACKING VARIABLES
# ==========================================

track_to_visitor = {}

last_seen_frame = {}

last_face_crop = {}

active_visitors = set()

unique_visitors = set()


# ==========================================
# PROCESS VIDEO
# ==========================================

results = model.track(
    source=VIDEO_SOURCE,
    tracker="bytetrack.yaml",
    persist=True,
    stream=True
)


frame_number = 0


for result in results:

    frame_number += 1

    frame = result.orig_img.copy()

    boxes = result.boxes

    current_track_ids = set()


    # ======================================
    # PROCESS DETECTED FACES
    # ======================================

    if boxes is not None and boxes.id is not None:

        for box, track_id in zip(
            boxes.xyxy,
            boxes.id
        ):

            track_id = int(
                track_id.item()
            )

            current_track_ids.add(
                track_id
            )

            last_seen_frame[
                track_id
            ] = frame_number


            # ------------------------------
            # FACE BOUNDING BOX
            # ------------------------------

            x1, y1, x2, y2 = map(
                int,
                box.tolist()
            )

            x1 = max(
                0,
                x1
            )

            y1 = max(
                0,
                y1
            )

            x2 = min(
                frame.shape[1],
                x2
            )

            y2 = min(
                frame.shape[0],
                y2
            )


            face_crop = frame[
                y1:y2,
                x1:x2
            ]


            # ==================================
            # IDENTIFY NEW TRACK
            # ==================================

            if (
                track_id
                not in track_to_visitor
                and face_crop.size > 0
            ):

                faces = face_app.get(
                    face_crop
                )


                if len(faces) > 0:

                    embedding = faces[
                        0
                    ].embedding


                    # --------------------------
                    # EMBEDDING LOG
                    # --------------------------

                    write_event_log(
                        "EMBEDDING_GENERATED",
                        "UNKNOWN",
                        track_id
                    )


                    # --------------------------
                    # IDENTIFY VISITOR
                    # --------------------------

                    (
                        visitor_id,
                        similarity,
                        is_new
                    ) = identify_visitor(
                        embedding,
                        visitors
                    )


                    track_to_visitor[
                        track_id
                    ] = visitor_id


                    last_face_crop[
                        track_id
                    ] = face_crop.copy()


                    unique_visitors.add(
                        visitor_id
                    )


                    # --------------------------
                    # TRACKING STARTED
                    # --------------------------

                    write_event_log(
                        "TRACKING_STARTED",
                        visitor_id,
                        track_id
                    )


                    # ==================================
                    # NEW VISITOR
                    # ==================================

                    if is_new:

                        visitors.append(
                            (
                                visitor_id,
                                embedding
                            )
                        )


                        print(
                            f"Track ID {track_id} -> "
                            f"{visitor_id} -> "
                            f"NEW VISITOR"
                        )


                        write_event_log(
                            "REGISTRATION",
                            visitor_id,
                            track_id
                        )


                    # ==================================
                    # RECOGNIZED VISITOR
                    # ==================================

                    else:

                        print(
                            f"Track ID {track_id} -> "
                            f"{visitor_id} -> "
                            f"RECOGNIZED "
                            f"(Similarity: "
                            f"{similarity:.4f})"
                        )


                        write_event_log(
                            "RECOGNITION",
                            visitor_id,
                            track_id,
                            similarity=similarity
                        )


                    # ==================================
                    # ENTRY EVENT
                    # ==================================

                    if (
                        visitor_id
                        not in active_visitors
                    ):

                        create_entry_event(
                            visitor_id,
                            face_crop,
                            track_id
                        )

                        active_visitors.add(
                            visitor_id
                        )


            # ==================================
            # SAVE LAST FACE IMAGE
            # ==================================

            if face_crop.size > 0:

                last_face_crop[
                    track_id
                ] = face_crop.copy()


            # ==================================
            # DISPLAY LABEL
            # ==================================

            visitor_id = track_to_visitor.get(
                track_id,
                "Identifying..."
            )


            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )


            label = (
                f"Track: {track_id} | "
                f"Visitor: {visitor_id}"
            )


            cv2.putText(
                frame,
                label,
                (
                    x1,
                    max(
                        20,
                        y1 - 10
                    )
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )


    # ==========================================
    # EXIT DETECTION
    # ==========================================

    for track_id in list(
        track_to_visitor.keys()
    ):

        if track_id not in current_track_ids:

            frames_missing = (
                frame_number
                -
                last_seen_frame.get(
                    track_id,
                    frame_number
                )
            )


            if (
                frames_missing
                >= EXIT_TIMEOUT_FRAMES
            ):

                visitor_id = (
                    track_to_visitor[
                        track_id
                    ]
                )


                if (
                    visitor_id
                    in active_visitors
                ):

                    print(
                        f"EXIT DETECTED | "
                        f"Visitor: {visitor_id} | "
                        f"Track: {track_id}"
                    )


                    if (
                        track_id
                        in last_face_crop
                    ):

                        create_exit_event(
                            visitor_id,
                            last_face_crop[
                                track_id
                            ],
                            track_id
                        )


                    active_visitors.remove(
                        visitor_id
                    )


                del track_to_visitor[
                    track_id
                ]


                if (
                    track_id
                    in last_seen_frame
                ):

                    del last_seen_frame[
                        track_id
                    ]


                if (
                    track_id
                    in last_face_crop
                ):

                    del last_face_crop[
                        track_id
                    ]


    # ==========================================
    # UNIQUE VISITOR COUNT
    # ==========================================

    cv2.putText(
        frame,
        f"Unique Visitors: "
        f"{len(unique_visitors)}",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2
    )


    # ==========================================
    # DISPLAY
    # ==========================================

    cv2.imshow(
        "Intelligent Face Tracker",
        frame
    )


    if (
        cv2.waitKey(1)
        & 0xFF
        == ord("q")
    ):
        break


# ==========================================
# FINAL EXITS
# ==========================================

print()
print("Video ended.")


for visitor_id in list(
    active_visitors
):

    print(
        f"FINAL EXIT | "
        f"Visitor: {visitor_id}"
    )


    for (
        track_id,
        mapped_visitor
    ) in track_to_visitor.items():

        if (
            mapped_visitor
            == visitor_id
        ):

            if (
                track_id
                in last_face_crop
            ):

                create_exit_event(
                    visitor_id,
                    last_face_crop[
                        track_id
                    ],
                    track_id
                )

            break


active_visitors.clear()

cv2.destroyAllWindows()


# ==========================================
# FINAL RESULT
# ==========================================

print()
print("================================")
print("Recognition completed!")
print(
    "Unique visitors:",
    len(unique_visitors)
)
print("================================")