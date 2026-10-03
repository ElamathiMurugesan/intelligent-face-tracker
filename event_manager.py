import os
import cv2
import json
from datetime import datetime

from database import log_event


# Load configuration
with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)


ENTRY_DIRECTORY = config["entry_log_directory"]
EXIT_DIRECTORY = config["exit_log_directory"]
EVENT_LOG = config["event_log"]


def write_event_log(
    event_type,
    visitor_id,
    track_id,
    image_path="",
    similarity=None
):
    os.makedirs(
        os.path.dirname(EVENT_LOG),
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    message = (
        f"{timestamp} | {event_type} | "
        f"Visitor: {visitor_id} | "
        f"Track: {track_id}"
    )

    if similarity is not None:
        message += (
            f" | Similarity: {similarity:.4f}"
        )

    if image_path:
        message += (
            f" | Image: {image_path}"
        )

    with open(
        EVENT_LOG,
        "a",
        encoding="utf-8"
    ) as file:
        file.write(message + "\n")

    if visitor_id != "UNKNOWN":
        log_event(
            visitor_id,
            event_type
        )


def create_entry_event(
    visitor_id,
    frame,
    track_id
):
    os.makedirs(
        ENTRY_DIRECTORY,
        exist_ok=True
    )

    timestamp = datetime.now()

    filename = (
        f"{visitor_id}_"
        f"{timestamp.strftime('%Y%m%d_%H%M%S')}.jpg"
    )

    image_path = os.path.join(
        ENTRY_DIRECTORY,
        filename
    )

    cv2.imwrite(
        image_path,
        frame
    )

    message = (
        f"ENTRY | Visitor: {visitor_id} | "
        f"Track: {track_id} | "
        f"Image: {image_path}"
    )

    print(message)

    write_event_log(
        "ENTRY",
        visitor_id,
        track_id,
        image_path=image_path
    )

    return image_path


def create_exit_event(
    visitor_id,
    frame,
    track_id
):
    os.makedirs(
        EXIT_DIRECTORY,
        exist_ok=True
    )

    timestamp = datetime.now()

    filename = (
        f"{visitor_id}_"
        f"{timestamp.strftime('%Y%m%d_%H%M%S')}.jpg"
    )

    image_path = os.path.join(
        EXIT_DIRECTORY,
        filename
    )

    cv2.imwrite(
        image_path,
        frame
    )

    message = (
        f"EXIT | Visitor: {visitor_id} | "
        f"Track: {track_id} | "
        f"Image: {image_path}"
    )

    print(message)

    write_event_log(
        "EXIT",
        visitor_id,
        track_id,
        image_path=image_path
    )

    return image_path