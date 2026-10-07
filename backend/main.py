from datetime import datetime
from typing import Literal
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()                      # the server object

# CORS lets your React app (a different port) call this API
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

# The shape of one location record; FastAPI validates incoming JSON against it
class Location(BaseModel):
    device_id: str
    latitude: float
    longitude: float
    timestamp: datetime
    status: Literal["online", "offline"]

locations: list[Location] = []       # temporary in-memory storage

@app.get("/")
def root():
    return {"message": "Tracker API is running"}

@app.post("/locations", status_code=201)   # device sends data here
def add_location(loc: Location):
    locations.append(loc)
    return loc

@app.get("/locations")                      # dashboard reads data here
def get_locations():
    return locations

@app.get("/locations/{device_id}/latest")   # latest point for one device
def latest(device_id: str):
    mine = [l for l in locations if l.device_id == device_id]
    return mine[-1] if mine else {"error": "not found"}