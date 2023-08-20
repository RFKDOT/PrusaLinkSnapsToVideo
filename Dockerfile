FROM python:3.10

WORKDIR /app

RUN pip3 install opencv-python requests python-dotenv

COPY . /app

CMD ["python3", "PrusaLinkGetSnaps.py"]