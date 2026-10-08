import os
from datetime import datetime, timezone
from typing import Literal

import pymysql
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

load_dotenv()                            # reads the .env file

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])


class Location(BaseModel):
    device_id: str = Field(min_length=1, max_length=50)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    timestamp: datetime
    status: Literal["online", "offline"]


def get_conn():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


def init_db():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
                        cur.execute("""
                CREATE TABLE IF NOT EXISTS locations (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    device_id VARCHAR(50) NOT NULL,
                    latitude DOUBLE NOT NULL,
                    longitude DOUBLE NOT NULL,
                    timestamp DATETIME NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    received_at DATETIME NOT NULL DEFAULT (UTC_TIMESTAMP),
                    INDEX idx_device_time (device_id, timestamp)
                )
            """)
    finally:
        conn.close()


init_db()                                 # creates the table on startup


@app.get("/")
def root():
    return {"message": "Tracker API is running"}


@app.post("/locations", status_code=201)
def add_location(loc: Location):
    ts = loc.timestamp
    if ts.tzinfo is not None:             # store everything as UTC
        ts = ts.astimezone(timezone.utc).replace(tzinfo=None)
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO locations (device_id, latitude, longitude, timestamp, status) "
                "VALUES (%s, %s, %s, %s, %s)",
                (loc.device_id, loc.latitude, loc.longitude, ts, loc.status),
            )
    finally:
        conn.close()
    return loc


@app.get("/locations")
def get_locations():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM locations ORDER BY id")
            return cur.fetchall()
    finally:
        conn.close()


@app.get("/locations/{device_id}/latest")
def latest(device_id: str):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM locations WHERE device_id = %s ORDER BY id DESC LIMIT 1",
                (device_id,),
            )
            row = cur.fetchone()
    finally:
        conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return row