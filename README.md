# Incident Management System (IMS)

## Overview

This project implements a simplified Incident Management System ,It ingests high-frequency signals, groups them intelligently using Redis, creates incidents (Work Items), and enforces RCA before closure.

---

##  Features

* Signal ingestion API (`/signal`)
* Redis-based debouncing (group multiple signals → one incident)
* Work Item (Incident) creation in PostgreSQL
* MongoDB for raw signal storage
* Incident lifecycle:

  * OPEN → RESOLVED → CLOSED
* RCA enforcement before closing incidents
* Dockerized multi-service setup

---

## Architecture

Signal Flow:

Signal → FastAPI → Redis (debounce) → PostgreSQL (Work Items)
↘ MongoDB (Raw Signals)

---

##  Tech Stack

* FastAPI (Backend)
* PostgreSQL (Relational DB)
* MongoDB (NoSQL DB)
* Redis (Caching & Debouncing)
* Docker & Docker Compose

---

##  Run the Project

```bash
docker-compose up --build
```

---

##  API Documentation

Open:
http://localhost:8000/docs

---

##  Key Functionalities

### 1. Signal Ingestion

Accepts incoming signals and stores raw data in MongoDB.

### 2. Debouncing Logic

Groups multiple signals within a time window to avoid duplicate incident creation.

### 3. Work Item Creation

First signal creates a Work Item (incident); subsequent signals attach to the same incident.

### 4. RCA Enforcement

An incident cannot be CLOSED without adding RCA.

---

## Design Decisions

* Redis used for fast, in-memory grouping of signals
* MongoDB used for flexible raw signal storage
* PostgreSQL used for structured incident tracking
* Docker ensures easy reproducibility

---

## Non-Functional Improvements

* Modular architecture (separation of concerns)
* Containerized setup for easy deployment
* Handles high-frequency signal ingestion
* Clean and maintainable code structure

---

## Project Structure

```
backend/
docker-compose.yml
README.md
```

---

## _________________________________________Test from output ________________________________________________________


### Start the system

```bash
docker-compose up --build
```

Wait until:

```
Uvicorn running on http://0.0.0.0:8000
```

---

### 2️⃣ Open API Docs

```
http://localhost:8000/docs
```

After open test with below commands

## Sample Execution in Outputs

Below are actual outputs observed during testing using Swagger UI (`/docs`).

---

### Signal Ingestion (First Request)

**Input:**

```json id="zxqkq2"
{
  "component_id": "CACHE_CLUSTER_01",
  "severity": "P2",
  "message": "Latency spike"
}
```

**Output:**

```json id="7rjfsr"
{
  "message": "Signal processed",
  "status": "new_work_item_created",
  "work_item_id": 1
}
```

---

### 🔹 2. Debouncing (Second Request within time window)

**Same Input Sent Again**

**Output:**

```json id="g7e7py"
{
  "message": "Signal processed",
  "status": "merged_with_existing",
  "work_item_id": 1
}
```

Confirms multiple signals are grouped into a single incident.

---

### 🔹 3. Fetch Work Items

**Output:**

```json id="p4v4ka"
[
  {
    "id": 1,
    "component_id": "CACHE_CLUSTER_01",
    "status": "OPEN",
    "rca": null
  }
]
```

---

### 🔹 4. Attempt to Close Without RCA

**Output:**

```json id="3x1z2c"
{
  "error": "Cannot close without RCA"
}
```

System correctly enforces RCA requirement.

---

### 🔹 5. Add RCA

**Input:**

```
rca = Database overload
```

**Output:**

```json id="3a7j8q"
{
  "message": "RCA added"
}
```

---

### 🔹 6. Resolve Incident

**Output:**

```json id="jzrz7y"
{
  "message": "Status updated"
}
```

---

### 🔹 7. Close Incident (After RCA)

**Output:**

```json id="c87qqo"
{
  "message": "Status updated"
}
```

---

## Summary of Behavior

* First signal → creates incident
* Repeated signals → merged (debounced)
* Incident cannot be closed without RCA
* Lifecycle is strictly enforced




## _______________________ Test from any machine___________________

### Start the system

```bash
docker-compose up --build
```

Wait until:

```
Uvicorn running on http://0.0.0.0:8000
```

---

### 2️⃣ Open API Docs

```
http://localhost:8000/docs
```

---

### Test Signal Ingestion

Send a signal:

```bash
curl -X POST http://localhost:8000/signal \
-H "Content-Type: application/json" \
-d '{
  "component_id": "CACHE_CLUSTER_01",
  "severity": "P2",
  "message": "Latency spike"
}'
```

#### Expected Output (First Request)

```json
{
  "message": "Signal processed",
  "status": "new_work_item_created",
  "work_item_id": 1
}
```

---

### 4️⃣ Test Debouncing

Send the same request again within 60 seconds:

#### Expected Output

```json
{
  "message": "Signal processed",
  "status": "merged_with_existing",
  "work_item_id": 1
}
```

 Same `work_item_id` confirms debouncing

---

### Get Work Items

```bash
curl http://localhost:8000/work-items
```

#### Expected Output

```json
[
  {
    "id": 1,
    "component_id": "CACHE_CLUSTER_01",
    "status": "OPEN",
    "rca": null
  }
]
```

---

### Test RCA Enforcement (Important)

Try closing without RCA:

```bash
curl -X POST "http://localhost:8000/work-items/1/status?status=CLOSED"
```

#### Expected Output

```json
{
  "error": "Cannot close without RCA"
}
```

---

### Add RCA

```bash
curl -X POST "http://localhost:8000/work-items/1/rca?rca=Database overload"
```

#### Expected Output

```json
{
  "message": "RCA added"
}
```

---

### Resolve and Close

```bash
curl -X POST "http://localhost:8000/work-items/1/status?status=RESOLVED"
curl -X POST "http://localhost:8000/work-items/1/status?status=CLOSED"
```

####  Expected Output

```json
{
  "message": "Status updated"
}
```

---

##  What this proves

* High-frequency signals are grouped (debouncing)
* Only one incident is created per component
* RCA is mandatory before closure
* Full lifecycle is enforced correctly


##  Author

Jidin K +91 9946391848
jidink61@gmail.com
