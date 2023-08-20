# PrusaLinkSnapShotvideMaker

Captura y descarga forma local las fotos realizadas por PrusaLink mediante su API, en formato PNG.  
Y a partir de esas capturas, genera un video MP4.

## Instalación manual

- Clonar proyecto

```
git clone git@github.com:RFKDOT/PrusaLinkSnapsToVideo.git
```

- Instalar dependencias

```
pip3 install opencv-python requests python-dotenv
```

## Configuración

- Copia el fichero .env.example a .env
- Editalo e incluye la IP local de tu RaspBerry donde tengas instalado PrusaLink, por defecto 'prusalink.local'
- Tambien incluye tu Clave API, la puedes encontrar o generar en la sección de Ajustes de tu PrusaLink

## Instalación Docker Compose

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

## Ejecución y uso

### PrusaLinkGetSnaps.py

- Descarga los snapshots generados según la configuración de la cámara en PrusaLink
- Se mantiene en ejecución permanente

```
python3 PrusaLinkGetSnaps.py
```

### MakeVideoFromSnaps.py

- Genera un video MP4 montando en él los SnapsShots de un determinado proyecto, en orden.

```
python3 MakeVideoFromSnaps.py
```

# Devel

```
docker system prune -a
docker build -t plstv .
docker run -it plstv
```