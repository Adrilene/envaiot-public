import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()


def get_current_device(device_name, devices_list):
    current_device = None
    for device in devices_list:
        if device.name == device_name:
            current_device = device
    return current_device


def write_log(message):
    with open(f"../{os.getenv('LOGS_PATH')}", "a") as log_file:
        log_file.write(f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - {message}\n")
