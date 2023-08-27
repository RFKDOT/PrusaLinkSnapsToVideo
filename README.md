# PrusaLinkSnapShotvideMaker

[![Build and Publish Docker Image](https://github.com/RFKDOT/PrusaLinkSnapsToVideo/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/RFKDOT/PrusaLinkSnapsToVideo/actions/workflows/docker-publish.yml)

Download the SnapShots of the photos taken by PrusaLink through its API, in PNG format.  
And from these snapshots, it generates an MP4 video.  

## Manual Installation

- Clone project

```
git clone git@github.com:RFKDOT/PrusaLinkSnapsToVideo.git
```

- Install dependencies

```
pip3 install opencv-python requests python-dotenv
```

### Configuration

- Copy the file .env.example to .env
- Edit it and include the local IP of your RaspBerry where you have PrusaLink installed, by default 'prusalink.local'.
- Also include your API Key, you can find it or generate it in the Settings section of your PrusaLink.

### Use PrusaLinkGetSnaps.py

- Downloads the generated snapshots according to the camera configuration to PrusaLink.
- Keeps running permanently

```
python3 PrusaLinkGetSnaps.py
```

### Use MakeVideoFromSnaps.py

- Generate an MP4 video by assembling the SnapsShots of a given project, in order.

```
python3 MakeVideoFromSnaps.py
```

## Docker Compose installation

```
version: '3.9'
services:
  PrusaLinkSnapsToVideo:
    container_name: PrusaLinkSnapsToVideo
    image: ghcr.io/rfkdot/prusalinksnapstovideo:main
    volumes:
      - /docker/plstv:/app/media
    environment:
      TZ: 'Europe/Madrid'
      PRUSALINK_IP: "prusalink.local"
      PRUSALINK_API_KEY: "api_key_from_prusa_link"
      DEBUG: 0
      SLEEP_TIME: 10
    working_dir: /app
    restart: always
```
