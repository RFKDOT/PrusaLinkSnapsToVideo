FROM python:slim-bullseye

WORKDIR /app

RUN pip3 install opencv-python requests python-dotenv

COPY . /app

RUN mkdir -p /app/media/png

RUN mkdir -p /app/media/mp4

ENTRYPOINT ["python3", "PrusaLinkGetSnaps.py"]