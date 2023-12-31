import os
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

IP_ADDRESS = os.getenv("PRUSALINK_IP")
API_KEY = os.getenv("PRUSALINK_API_KEY")
DEBUG = bool(os.getenv("DEBUG", 1))
SLEEP_TIME = int(os.getenv("SLEEP_TIME", 1))

HEADERS = {"X-Api-Key": API_KEY}

sleep_time = SLEEP_TIME
previous_snapshot = None

def this_time():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")

def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def download_snapshot():
    global previous_snapshot, sleep_time

    try:
        job_response = requests.get(f"http://{IP_ADDRESS}/api/v1/job", headers=HEADERS)
        job_response.raise_for_status()
    except Exception as e:
         print(f"{this_time()} Printer is off !?!?", flush=True)
         sleep_time = 600
         return

    if job_response.status_code != 200:
        print(f"{this_time()} Printer is stand-by !?!?", flush=True)
        sleep_time = 120
        return

    job_data = job_response.json()

    job_name = job_data.get("file", {}).get("name", "")

    if ".gcode" in job_name:
        job_name = job_name.replace(".gcode", "")

    if ".gco" in job_name:
        job_name = job_name.replace(".gco", "")

    job_name = job_name.replace("   ", "_")
    job_name = job_name.replace("  ", "_")
    job_name = job_name.replace(" ", "_")

    snap_response = requests.get(f"http://{IP_ADDRESS}/api/v1/cameras/snap", headers=HEADERS)
    snap_response.raise_for_status()

    if previous_snapshot == snap_response.content:
        if DEBUG==True: print(f"{this_time()} Same image, waiting {sleep_time} seconds", flush=True)
        return

    else:
        previous_snapshot = snap_response.content

        time_printing = job_data.get("time_printing")
        formatted_time = format_time(time_printing)

        file_name = f"media/png/{job_name}_@_{formatted_time}_{time_printing}.png"
        with open(os.path.join(os.getcwd(), file_name), "wb") as file:
            file.write(snap_response.content)

        print(f"{this_time()} Image saved => {file_name}", flush=True)
        sleep_time = SLEEP_TIME

while True:

    try:
        download_snapshot()
        time.sleep(sleep_time)

    except Exception as e:
        print(f"Error: {e}", flush=True)
        time.sleep(sleep_time)
