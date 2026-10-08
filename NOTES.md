# Full Stack Starter Task - Concepts & Notes

## Core Software Concepts

- **Client vs Server:** The client (e.g., web browser, React dashboard, or GPS device) makes requests for data or actions. The server (e.g., FastAPI backend) processes those requests, interacts with the database, and returns a response.
- **HTTP (Hypertext Transfer Protocol):** The standardized communication protocol used for sending requests and responses between clients and servers across the web. Key components include HTTP methods (GET, POST), URLs, status codes (200, 404, 500), headers, and message bodies.
- **GET vs POST:** GET requests fetch or retrieve data from the server without modifying state. POST requests send data to the server to create or update resources (e.g., submitting device location telemetries).
- **REST API (Representational State Transfer):** An architectural style for web services where resources are identified using structured URLs (`/locations`) and standard HTTP methods define operations on those resources.
- **JSON (JavaScript Object Notation):** A lightweight, human-readable text format structured as key-value pairs used to transfer structured data between client and server.
- **Database:** Persistent storage designed to save, query, and retrieve structured data so that information survives server restarts (unlike in-memory server lists).

## Hardware & Communication Concepts

- **GPS (Global Positioning System):** A module that receives satellite signals to determine the exact latitude, longitude, and timestamp of the device.
- **IMU (Inertial Measurement Unit):** A sensor containing accelerometers and gyroscopes to track motion, orientation, and speed metrics.
- **Communication Module:** A hardware unit (such as cellular GSM, Wi-Fi, or LoRa) that wirelessly transmits sensor data to remote servers via network protocols.

---

## System Flow

### Diagram

```mermaid
flowchart LR
    A["DEVICE<br/>(GPS + IMU)"] -->|"WiFi / GSM"| B["NETWORK<br/>(Internet)"]
    B -->|"HTTP POST + JSON"| C["BACKEND API<br/>(FastAPI)"]
    C -->|"SQL INSERT / SELECT"| D[("DATABASE<br/>(MySQL)")]
    C -->|"HTTP GET + JSON"| E["DASHBOARD<br/>(React)"]
```

Text version:

```
DEVICE (GPS + IMU)
   |  WiFi / GSM
   v
NETWORK (Internet)
   |  HTTP POST + JSON
   v
BACKEND API (FastAPI)  <---- HTTP GET + JSON ----  DASHBOARD (React)
   |  SQL INSERT / SELECT
   v
DATABASE (MySQL)
```

### What each part does

| Part | Role | Technology |
|---|---|---|
| Device | Reads position (GPS) and motion (IMU), builds a JSON message | GPS module + IMU sensor + microcontroller |
| Network | Carries the data from the device to the server | WiFi / GSM / 4G |
| Backend API | Receives data, validates it, stores it, serves it to the dashboard | FastAPI (Python) |
| Database | Stores location records permanently | MySQL (`tracker_db`, table `locations`) |
| Dashboard | Fetches data and shows it to the user | React (Vite) |

### Step-by-step journey of one location update

1. The **GPS** gives latitude and longitude. The **IMU** gives motion data.
2. The device packs the data into **JSON**:

   ```json
   {
     "device_id": "DEVICE001",
     "latitude": 10.0000,
     "longitude": 78.0000,
     "timestamp": "2026-10-06T10:00:00Z",
     "status": "online"
   }
   ```

3. The device sends it through the **network** (WiFi/GSM) as an **HTTP POST** to `/locations`.
4. The **FastAPI backend** validates the JSON against the `Location` model. Invalid data gets a **422** error.
5. If valid, the backend **stores** it in MySQL and returns **201 Created**.
6. The **React dashboard** sends an **HTTP GET** to `/locations` every 5 seconds.
7. The backend reads the rows from MySQL and returns them as JSON with **200 OK**.
8. React saves them in state and **re-renders the table**, so the new location appears.

### What travels on each arrow

| Arrow | What travels |
|---|---|
| Device -> Network | Data packets over WiFi/GSM |
| Network -> API | HTTP POST request with a JSON body |
| API -> Database | SQL INSERT with the validated fields |
| Database -> API | Rows from a SQL SELECT |
| API -> Dashboard | HTTP 200 response with a JSON list |

### Who is the client and who is the server?

- **Server:** the FastAPI backend, which waits for requests.
- **Clients:** the device (sends data with POST) and the dashboard (reads data with GET).

---

## What I Built

- A FastAPI backend with `POST /locations`, `GET /locations`, and `GET /locations/{device_id}/latest`
- A `Location` model that validates `device_id`, `latitude`, `longitude`, `timestamp`, and `status`
- A MySQL database (`tracker_db`) with a `locations` table, created automatically by the backend on startup
- A React dashboard (Vite) that fetches data from the backend every 5 seconds and shows it in a table
- Database credentials kept in a `.env` file (ignored by Git), with a `.env.example` showing the required settings
- A README with setup steps, API endpoints, example JSON, and screenshots

## Testing Done

| Test | Result |
|---|---|
| POST a valid record at `/docs` and Postman | Returns 201 and the record is saved |
| POST invalid data (text latitude) | Returns 422 with a validation message |
| Check the record in MySQL Workbench | Row with device_id and all fields is visible |
| Stop the backend, start it again, GET `/locations` | Record is still there, so MySQL persistence works |
| POST a new record while the dashboard is open | Row appears within 5 seconds without refreshing |

## Problems I Faced and How I Fixed Them

- **`{"detail":"Not Found"}`:** I opened `/`, which has no route (404). The correct URLs are `/docs` and `/locations`.
- **CORS:** Browsers block requests between different ports unless the backend allows them, so I added `CORSMiddleware`.
- **Data lost on restart:** The list lived in memory, so data disappeared when the server restarted. I moved to MySQL for persistence.
- **`uvicorn` not recognized:** The virtual environment was not active and I was in the wrong folder. Fix: `cd backend`, then `venv\Scripts\activate`, then run `uvicorn`.
- **`git add` could not find `NOTES.md`:** I was inside `backend`, but the file is in `tracker`. Fix: `cd ..` first. Always check the current folder before running Git commands.
- **Password in `.env.example`:** I had put my real database password in a file pushed to GitHub. Fix: changed the MySQL password, replaced it with a placeholder, and learned that real secrets belong only in `.env`.
- **Wrong GitHub account:** The repo was linked to the wrong account. Fix: removed the saved login in Credential Manager, changed the remote with `git remote set-url`, and set `git config user.name` and `user.email`.
- **Could not see the folder tree in VS Code:** Only the "Open Editors" section was showing. Fix: collapse it and open the project folder section.

## What I Learned

- **How data flows:** The device sends its location as JSON, the backend checks it and saves it in MySQL, and the dashboard asks the backend for the saved data and shows it in a table.
- **POST vs GET:** The device uses POST because it sends new data to be stored. The dashboard uses GET because it only reads data and changes nothing.
- **Validation:** A 422 error means the request was understood but the data was invalid, for example text instead of a number. This protects the database from bad data.
- **Database:** Data in a Python list disappears when the server stops. Data in MySQL stays, which I proved by restarting the backend and seeing the record still there.
- **Security:** Passwords go in `.env`, which is listed in `.gitignore`. `.env.example` is committed with placeholder values only, so others know which settings to fill in.
- **Git routine:** `git status`, `git add .`, `git status`, `git commit -m "message"`, `git push`. Always read `git status` before committing, and check which folder I am in.
- **Debugging:** Read the error message and the terminal prompt carefully. Most of my problems were a wrong folder, an inactive virtual environment, or a wrong setting, not broken code.

---

## Current Limitations and Next Steps

- The dashboard polls every 5 seconds. Later: WebSockets for live updates.
- Offline status is sent by the device. Better: the backend marks a device offline if no update arrives for 60 seconds.
- CORS currently allows all origins. In production it should allow only the dashboard's address.
- Next features: a device simulator that sends fake moving data, and a map view (`react-leaflet`).

##DAY 2:
What happens to a location from the moment the ESP32 sends it to the moment it shows on the dashboard?

The location is sent in HTTP POST(JSON format) from the ESP32 to the backend which is made of FastAPI. this file is verified that whether the location is in the required format or not . if it is in the required format then the JSON is sent to be posted into the Database(postgreSQL or MySQL). the Data base like a record bokk which contains all the locations till now even the backend is not running. whenever a DashBoard(react or Futter) is loaded then it request the backend throught RestAPI's (GET) to provide the data from the database to display on the dashboard. 
