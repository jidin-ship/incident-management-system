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

##  Author

Jidin K +91 9946391848
