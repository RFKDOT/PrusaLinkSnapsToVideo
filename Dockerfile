FROM python:slim-bullseye

WORKDIR /app

RUN pip3 install opencv-python requests python-dotenv

COPY . /app

ENTRYPOINT ["tail", "-f", "/dev/null"]

# CMD ["python3", "PrusaLinkGetSnaps.py"]

# CMD ["sleep", "infinity"]