import sqlite3
import numpy as np
from datetime import datetime
import os
import json


# ==========================================
# LOAD CONFIGURATION
# ==========================================

with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

DATABASE = config["database_path"]


# ==========================================
# CREATE DATABASE
# ==========================================

def create_database():

    os.makedirs(
        os.path.dirname(DATABASE),
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE
    )

    cursor = connection.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visitors (
            visitor_id TEXT PRIMARY KEY,
            embedding BLOB NOT NULL,
            first_seen TEXT NOT NULL,
            last_seen TEXT NOT NULL
        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visitor_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)


    connection.commit()
    connection.close()


# ==========================================
# REGISTER VISITOR
# ==========================================

def register_visitor(embedding):

    create_database()

    connection = sqlite3.connect(
        DATABASE
    )

    cursor = connection.cursor()


    cursor.execute(
        "SELECT visitor_id FROM visitors"
    )

    rows = cursor.fetchall()


    if len(rows) == 0:

        visitor_id = "V001"

    else:

        numbers = []

        for row in rows:

            number = int(
                row[0][1:]
            )

            numbers.append(
                number
            )

        visitor_id = (
            f"V{max(numbers) + 1:03d}"
        )


    timestamp = datetime.now().isoformat()


    embedding_bytes = np.array(
        embedding,
        dtype=np.float32
    ).tobytes()


    cursor.execute("""
        INSERT INTO visitors
        (visitor_id, embedding, first_seen, last_seen)
        VALUES (?, ?, ?, ?)
    """, (
        visitor_id,
        embedding_bytes,
        timestamp,
        timestamp
    ))


    connection.commit()
    connection.close()


    return visitor_id


# ==========================================
# LOAD VISITORS
# ==========================================

def load_visitors():

    create_database()

    connection = sqlite3.connect(
        DATABASE
    )

    cursor = connection.cursor()


    cursor.execute(
        "SELECT visitor_id, embedding FROM visitors"
    )

    rows = cursor.fetchall()

    connection.close()


    visitors = []


    for visitor_id, embedding_blob in rows:

        embedding = np.frombuffer(
            embedding_blob,
            dtype=np.float32
        )

        visitors.append(
            (
                visitor_id,
                embedding
            )
        )


    return visitors


# ==========================================
# LOG EVENT INTO DATABASE
# ==========================================

def log_event(
    visitor_id,
    event_type
):

    create_database()

    connection = sqlite3.connect(
        DATABASE
    )

    cursor = connection.cursor()


    timestamp = datetime.now().isoformat()


    cursor.execute("""
        INSERT INTO events
        (visitor_id, event_type, timestamp)
        VALUES (?, ?, ?)
    """, (
        visitor_id,
        event_type,
        timestamp
    ))


    connection.commit()
    connection.close()