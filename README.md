# Dockerized Wake-on-LAN Auto-Monitor

## Overview

This project provides a **Dockerized Wake-on-LAN (WoL) monitor** that automatically wakes up a machine on your network if it becomes unreachable.

It continuously **pings the target machine**.  
If the machine is offline, it sends a **WoL magic packet** using `etherwake` to power it on remotely.

---

## How It Works

1. Periodically **pings the target machine** via ICMP.
2. If the target is **online**, it logs the status.
3. If the target is **offline**, it sends a **WoL magic packet** using `etherwake`.
4. Optionally, you can specify the **network interface** using `WOL_INTERFACE`.
5. The process repeats at a configurable interval.

---

## Environment Variables

Create a `.env` file in the root directory:

| Variable        | Description                                          |
|-----------------|------------------------------------------------------|
| `TARGET_IP`     | **IPv4 address** of the machine to monitor           |
| `TARGET_MAC`    | **MAC address** of the target machine                |
| `CHECK_INTERVAL`| Interval (in seconds) between checks (default: `30`) |
| `WOL_INTERFACE` | (Optional) **Network interface** for WoL packets     |

---

### Example `.env`

```env
TARGET_IP=192.168.1.50
TARGET_MAC=AA:BB:CC:DD:EE:FF
CHECK_INTERVAL=60
WOL_INTERFACE=eth0
```

---

## Project Structure

| File                 | Description                                   |
|----------------------|-----------------------------------------------|
| `.env`               | Environment variables                         |
| `wakeonlan.py`       | Python script that handles monitoring and WoL |
| `Dockerfile`         | Docker build instructions                     |
| `docker-compose.yml` | Service orchestration                         |

---

## Dockerfile

```Dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y etherwake iputils-ping && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY wakeonlan.py /app/wakeonlan.py

WORKDIR /app

CMD ["python", "wakeonlan.py"]
```

---

## Docker Compose

```yaml
services:
  wakeonlan:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: wakeonlan
    env_file:
      - .env
    network_mode: "host"
    restart: unless-stopped
    privileged: true
```

---

## Usage

### 1. Build the Docker Image

```bash
docker-compose build
```

---

### 2. Run the Service

```bash
docker-compose up -d
```

---

### 3. View Logs

```bash
docker-compose logs -f
```

---

## WoL Interface Behavior

- If `WOL_INTERFACE` is set, the WoL packet will be sent using:

```bash
etherwake -b -i <WOL_INTERFACE> <TARGET_MAC>
```

- If `WOL_INTERFACE` is not set:

```bash
etherwake -b <TARGET_MAC>
```

---

## Requirements

- Your target machine must support **Wake-on-LAN** and have it enabled in BIOS/UEFI.
- Docker must run in **host network mode** for WoL to work properly.
- The container runs with `privileged: true` to allow raw packet sending.

---

## Summary

This service lets you automatically monitor and wake up machines on your network using Docker.  
It is ideal for **home servers, NAS systems, remote PCs, and lab environments** where uptime is critical.

---
