# Unit3DupWeb

![version](https://img.shields.io/pypi/v/unit3dupWeb.svg)
![online](https://img.shields.io/badge/Online-green)
![status](https://img.shields.io/badge/Status-Active-brightgreen)
![python](https://img.shields.io/badge/Python-3.12+-blue)
![ubuntu](https://img.shields.io/badge/Ubuntu-22+-blue)
![debian](https://img.shields.io/badge/Debian-12+-blue)
![windows](https://img.shields.io/badge/Windows-11-blue)

---

# Auto Torrent Generator and Uploader

Reworked from the original [Unit3Dup](https://github.com/31December99/Unit3Dup)

This code is under testing.

![Home](images/home.png)

---

## Demo video

[Here](https://streamable.com/agoizj)

---

## What it does

* Scan folder and subfolders
* Compiles metadata to create a torrent
* Extracts screenshots from video
* Adds webp images to torrent page description
* Searches IDs on TMDB, IMDb, TVDB
* Adds trailer from TMDB or YouTube
* Seeds in qBittorrent
* Generates metadata from video
* Creates and uploads torrents/pages

---

## NOT YET TESTED

* Extracts cover from PDF documents
* Reseeding multiple torrents
* Cross-OS seeding
* Custom season titles
* MediaInfo-based metadata generation
* Extract first page of PDFs via xpdf and upload it
* Windows support improvements

---

## NOT YET IMPLEMENTED

* Game metadata generation
* Transmission / rTorrent seeding

---

## Install from Docker Hub

* Complete `.env.example`
* Rename to `.env`
* Run:

```bash
docker-compose pull
```

---

## How it works

The backend provides FastAPI endpoints.

For each video file, a job_id is generated from the hash of its path.

* job_ids form a job_list (page view)
* each page has a job_list_id based on scan path hash

WebSocket is used for:

* progress updates
* logs to frontend

### Scan process

* Search files/folders
* Extract title
* Query TMDB (movie/series)
* Query TVDB and get IMDb ID
* Create screenshots
* Build description with MediaInfo + screenshots

### Editing

If poster has issues (TMDB/IMDb mismatch):

* click poster
* edit fields
* create torrent / upload / seed

---

## Frontend build

```bash
flutter pub get
flutter build web --release --wasm
```

---

## Backend build

```bash
docker-compose -f build.yml build --no-cache
docker-compose up
```

---

## Docker Hub

```bash
docker login

docker tag unit3dwebup-backend:latest parzival2025/backend_app:x.y.z
docker tag unit3dwebup-frontend:latest parzival2025/frontend_app:x.y.z

docker push parzival2025/backend_app:x.y.z
docker push parzival2025/frontend_app:x.y.z
```

---

## Trackers

The Italian tracker community: people with technical and social backgrounds
united by torrents.

| Tracker | Description                                          |
| ------- | ---------------------------------------------------- |
| ITT     | [https://itatorrents.xyz/](https://itatorrents.xyz/) |

---

## Discord

[Join Discord](https://discord.gg/8RpwN2Khcz)

![Discord](https://img.shields.io/discord/1214696147600408698?label=Discord\&logo=discord\&style=flat)

---

## AstraeLabs

[GitHub Project](https://github.com/AstraeLabs/VibraVid)

Open-source script for downloading movies, TV shows, and anime.

![AstraeLabs](https://img.shields.io/badge/AstraeLabs-blue.svg)
