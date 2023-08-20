import os
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

IP_ADDRESS = os.getenv("PRUSALINK_IP")
API_KEY = os.getenv("PRUSALINK_API_KEY")
DEBUG = os.getenv("DEBUG", 1)
SLEEP_TIME = int(os.getenv("SLEEP_TIME", 1))

HEADERS = {"X-Api-Key": API_KEY}

sleep_time = SLEEP_TIME
previous_snapshot = None
snapshot_counter = 0

def this_time():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")

def initialize():
    try:
        info_response = requests.get(f"http://{IP_ADDRESS}/api/v1/info", headers=HEADERS)
        info_response.raise_for_status()
        return True
    except Exception as e:
        print(f"{this_time()} Error: {e}", flush=True)
        return False

def format_time(seconds):
    """Format time in seconds to HH:MM:SS"""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def download_snapshot():
    global previous_snapshot
    global sleep_time

    job_response = requests.get(f"http://{IP_ADDRESS}/api/v1/job", headers=HEADERS)
    job_response.raise_for_status()

    if job_response.status_code != 200:
        print(f"{this_time()} Parece que en este momento no se está imprimiendo nada", flush=True)
        sleep_time = 120
        return

    # print(job_response.json())
    job_data = job_response.json()

    job_name = job_data.get("file", {}).get("name", "")

    if ".gcode" in job_name:
        job_name = job_name.replace(".gcode", "")

    if ".gco" in job_name:
        job_name = job_name.replace(".gco", "")

    snap_response = requests.get(f"http://{IP_ADDRESS}/api/v1/cameras/snap", headers=HEADERS)
    snap_response.raise_for_status()

    if previous_snapshot != snap_response.content:
        previous_snapshot = snap_response.content

        time_printing = job_data.get("time_printing")
        formatted_time = format_time(time_printing)

        file_name = f"media/png/{job_name}_@_{formatted_time}_{time_printing}.png"
        with open(os.path.join(os.getcwd(), file_name), "wb") as file:
            file.write(snap_response.content)

        print(f"{this_time()} Captura obtenida y almacenada en {file_name}", flush=True)
        sleep_time = SLEEP_TIME

    else:
        if DEBUG == 1:
            print(f"{this_time()} Misma captura, esperamos {sleep_time} segundos", flush=True)

if initialize() is False:
    print(f"{this_time()} Parece que no hay conexión con la impresora", flush=True)
    sleep_time = 300
    exit()

while True:
    try:
        download_snapshot()
        time.sleep(sleep_time)

    except Exception as e:
        print(f"Error: {e}", flush=True)
        time.sleep(sleep_time)
