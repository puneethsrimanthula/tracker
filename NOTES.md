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