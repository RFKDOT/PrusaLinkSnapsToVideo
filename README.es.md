# PrusaLinkSnapShotvideMaker

[![Build and Publish Docker Image](https://github.com/RFKDOT/PrusaLinkSnapsToVideo/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/RFKDOT/PrusaLinkSnapsToVideo/actions/workflows/docker-publish.yml)

Descarga los SnapShots de las fotos tomadas por PrusaLink a través de su API, en formato PNG.  
Y a partir de estas instantáneas genera un vídeo MP4.

## Instalación manual

-   Clonar proyecto


    git clone git@github.com:RFKDOT/PrusaLinkSnapsToVideo.git

-   Instalar dependencias


    pip3 install opencv-python requests python-dotenv

### Configuración

-   Copie el archivo .env.example a .env
-   Edítalo e incluye la IP local de tu RaspBerry donde tienes instalado PrusaLink, por defecto 'prusalink.local'.
-   Incluye también tu clave API, puedes encontrarla o generarla en la sección Configuración de tu PrusaLink.

### Utilice PrusaLinkGetSnaps.py

-   Descarga las instantáneas generadas según la configuración de la cámara a PrusaLink.
-   Sigue funcionando permanentemente


    python3 PrusaLinkGetSnaps.py

### Utilice MakeVideoFromSnaps.py

-   Genere un video MP4 ensamblando las instantáneas de un proyecto determinado, en orden.


    python3 MakeVideoFromSnaps.py

## Instalación de Docker Compose

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
